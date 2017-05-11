import yaml
from optparse import OptionParser
from mako.template import Template


parser = OptionParser(usage="%prog [options]")
parser.add_option("-c", "--config",
                  action="store",
                  type="string",
                  dest="config",
                  help="Specify configuration file path")
parser.add_option('-t',
               action="store_true",
               dest="test",
               default=False,
               help="Test configuration file format")

(options, args) = parser.parse_args()

if not options.config:
    print('error: Configuration file is required, use the -c parameter to specify the configuration file path')
    exit(-1)

if options.test:
    with open(options.config) as f:
        try:
            x = yaml.load(f)
        except Exception,e:
            print("test config file %s failed" % options.config)
            print(e)
            exit(-1)
        else:
            print("test config file %s success"%options.config)
            exit(0)


with open(options.config) as f:
    config = yaml.load(f)
    zhtemplate = Template(filename=config['templete']['templateFile_zh_CN'],
                          input_encoding='utf-8',
                          output_encoding='utf-8',
                          encoding_errors='replace')
    #print config['template']
    print zhtemplate.render(**config['templete'])



