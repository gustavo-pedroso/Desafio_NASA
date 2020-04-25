import pathlib
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType
from nasa_log_parser import log_parser

# defining the base folder for better portability and readability
base_folder = str(pathlib.Path(__file__).parent.parent.absolute()).replace('\\', '/')

# creating the spark session
spark = SparkSession.builder.appName("Desafio_Nasa").getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# setting the file names for the data that will be used
log_Jul95 = base_folder + '/data/NASA_access_log_Jul95/access_log_Jul95'
log_Aug95 = base_folder + '/data/NASA_access_log_Aug95/access_log_Aug95'

# creating file names for the parsed files
parsed_Jul95 = base_folder + '/data/NASA_access_log_Jul95/Jul95_parsed.csv'
parsed_Aug95 = base_folder + '/data/NASA_access_log_Aug95/Aug95_parsed.csv'

# call to nasa_log_paser.log_parser to parse the log files into column delimited files (csv)
log_parser(log_Jul95, parsed_Jul95)
log_parser(log_Aug95, parsed_Aug95)

# using the spark session object to read the files and their headers
df_Jul95 = spark.read.csv(parsed_Jul95, header=True)
df_Aug95 = spark.read.csv(parsed_Aug95, header=True)

# print dataframe schemas in order to verify compatibility for merging later
print('Schema for df_Jul95:')
print(df_Jul95.printSchema())
print('Schema for df_Aug95:')
print(df_Aug95.printSchema())

# basic count of number of records in each of the dataframes
print('Number of records for Jul 95: {}'.format(df_Jul95.count()))
print('Number of records for Aug 95: {}'.format(df_Aug95.count()))

# unionAll of both data in order to merge the dataframes into a single one
df = df_Jul95.unionAll(df_Aug95)
# show final parsed dataframe
print('Sample of final dataframe:')
df.show(5, False)

# simple select using distinc and count to get unique hosts
print('Question 1: Numero de hosts unicos')
print('Total distinct hosts: {}'.format(df.select('requester').distinct().count()))

# dataframe filter and count to get total amount of 404 errors
print('Question 2: O total de erros 404')
print('Total 404 responses: {}'.format(df.filter('response == "404"').count()))

# first filter 404 errors, than group by resource and count
print('Question 3: Os 5 URLs que mais causaram erro 404')
print(df.filter('response == "404"').groupBy('resource').agg(F.count('response')).orderBy(F.desc('count(response)')).
      show(5, False))


# a little more complicate since timestamp had to be converted using date_utils.py and UDF (user defined function)
# simple method to convert string timestamp to a python friendly format
def convert_timestamp(str_timestamp):
    from datetime import datetime
    try:
        return datetime.strptime(str_timestamp, '%d/%b/%Y:%H:%M:%S %z')
    except:
        # on exception return None, this will happen if the date string is malformed/corrupted
        return None


# create a UDF (user defined function) to use in the main class and apply to the timestamp column
convert_timestamp_udf = F.udf(lambda x: convert_timestamp(x), TimestampType())

# after converting, data is grouped by dayofyear, aggregated by count and date elements (dayofmonth, month, year)
df = df.withColumn('date_timestamp', convert_timestamp_udf('timestamp'))
temp = df.filter('response == "404"').groupBy(F.dayofyear('date_timestamp')).\
    agg(F.count('response'),
        F.max(F.dayofmonth('date_timestamp')),
        F.max(F.month('date_timestamp')),
        F.max(F.year('date_timestamp')))

# a new select is made to format the result using alias
temp = temp.select(F.concat('max(dayofmonth(date_timestamp))',
                            F.lit('/'),
                            'max(month(date_timestamp))',
                            F.lit('/'), 'max(year(date_timestamp))').alias('day'),
                   F.col('count(response)').alias('total_404'))

# finally order by date
temp = temp.orderBy('max(year(date_timestamp))', 'max(month(date_timestamp))', 'max(dayofmonth(date_timestamp))')
print('Question 4: Quantidade de erros 404 por dia')
temp.show(100, False)

# simple aggregation function to sum all bytes returned in all requests
print('Question 5: O total de bytes retornados')
print('Total bytes returned to requesters: {} bytes'.format(int(df.agg(F.sum('response_size')).collect()[0][0])))

# stop sparkSession (SparkContext) after code is finished
spark.stop()
exit(1)

