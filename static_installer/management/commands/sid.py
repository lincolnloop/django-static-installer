import os
import urllib2
from urlparse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import simplejson

class Command(BaseCommand):
    help = 'Installs the static dependencies from a file.'
    args = '<dependency dependency ...>'

    def handle(self, *args, **options):
        if not len(args):
            raise CommandError('You must at least specify one dependency file.')

        CURRENT_PATH = os.getcwd()
        paths = []

        for arg in args:
            dependency_path = os.path.join(CURRENT_PATH, arg)
            if not os.path.exists(dependency_path):
                raise CommandError('Could not load %s. File does not exist.' % dependency_path)

            paths.append(dependency_path)

        for path in paths:
            json_obj = simplejson.loads(open(path, 'r').read())

            for item in json_obj:
                install_dependencies(json_obj.get(item, None), os.path.join(settings.STATIC_ROOT_DEFAULT, item))



def install_dependencies(dependencies, path):

    for item in dependencies:
        if type(dependencies).__name__ == 'dict':
            folder = os.path.join(path, item)
            if not os.path.exists(folder):
                print "mkdir %s.." % (folder)
                os.mkdir(folder)

            install_dependencies(dependencies[item], os.path.join(path, item))
        else:
            parsed_url = urlparse(item)
            if parsed_url[5] and parsed_url[5].find('filename=') != -1:
                filename = parsed_url[5].replace('filename=', '')
            else:
                filename = parsed_url[2].split('/')[-1]

            print "downloading %s..." % item

            remote_file = urllib2.urlopen(item)
            local_file = open(os.path.join(path, filename), 'w')
            local_file.write(remote_file.read())
            local_file.close()

