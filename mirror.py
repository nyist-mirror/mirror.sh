from optparse import OptionParser
from mako.template import Template
import logging
import json
import time


parser = OptionParser(usage="%prog [options]")
parser.add_option("--name",
                  action="store",
                  type="string",
                  dest="name",
                  help="mirror name")

parser.add_option('--status',
               action="store",
               dest="status",
               type="string",
               help="exit code")

parser.add_option('--size',
               action="store",
               dest="size",
               type="string",
               help="dictory size")

parser.add_option('--num',
               action="store",
               dest="num",
               type="int",
               help="file num")

parser.add_option("--db",
                  action="store",
                  type="string",
                  dest="db",
                  help="db name")
parser.add_option("--log",
                  action="store",
                  type="string",
                  dest="log",
                  help="log file")

parser.add_option("--template",
                  action="store",
                  type="string",
                  dest="template",
                  help="template file")

parser.add_option("--out",
                  action="store",
                  type="string",
                  dest="out",
                  help="out file")

(options, args) = parser.parse_args()

if not options.log:
    raise Exception('error: log file size  is required, use the --log parameter to specify it')
    exit(-1)

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",datefmt='%F  %H:%M:%S',filename=options.log,filemode='a')

if not options.name:
    logging.error('error: Mirror name is required, use the --name parameter to specify the mirror name')
    raise Exception('error: Mirror name is required, use the --name parameter to specify the mirror name')
    exit(-1)

if not options.status:
    logging.error('error: Last task exit code is required, use the --status parameter to specify the exit code')
    raise Exception('error: Last task exit code is required, use the --status parameter to specify the exit code')
    exit(-1)

if not options.num:
    logging.error('error: Dictory file sum number  is required, use the --num parameter to specify it')
    raise Exception('error: Dictory file sum number  is required, use the --num parameter to specify it')
    exit(-1)

if not options.size:
    logging.error('error: Dictory file size  is required, use the --size parameter to specify it')
    raise Exception('error: Dictory file size  is required, use the --size parameter to specify it')
    exit(-1)

if not options.db:
    logging.error('error: Db file size  is required, use the --db parameter to specify it')
    raise Exception('error: Db file size  is required, use the --db parameter to specify it')
    exit(-1)



if not options.template:
    logging.error('error: template file   is required, use the --template parameter to specify it')
    raise Exception('error: template file   is required, use the --template parameter to specify it')
    exit(-1)

if not options.out:
    logging.error('error: out file   is required, use the --out parameter to specify it')
    raise Exception('error: out file   is required, use the --out parameter to specify it')
    exit(-1)


with open(options.db) as db:
    database = db.read()

try:
    data=json.loads(database)
except ValueError:
    logging.warning("the database is empty...")
    data={}


data[options.name]={'status':options.status,'num':options.num,'size':options.size,'time':str(time.strftime('%Y-%m-%d %H:%M:%S'))}

logging.info(data)

with open(options.db,'w') as db:
    db.write(json.dumps(data))
zhtemplate=Template(filename=options.template,input_encoding='utf-8',output_encoding='utf-8',encoding_errors='replace')

with open(options.out,'w') as out:
    out.write(zhtemplate.render(data=data))
