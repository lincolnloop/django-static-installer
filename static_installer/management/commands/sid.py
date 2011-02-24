import os
import urllib2

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
            object = simplejson.loads(open(path, 'r').read())

            for item in object:
                install_dependencies(object.get(item, None), os.path.join(settings.STATIC_ROOT_DEFAULT, item))



def install_dependencies(dependencies, path):

    for item in dependencies:
        if type(dependencies).__name__ == 'dict':
            dir = os.path.join(path, item)
            if not os.path.exists(dir):
                print "mkdir %s.." % (dir)
                os.mkdir(dir)

            install_dependencies(dependencies[item], os.path.join(path, item))
        else:
            #remotefile = urllib2.urlopen(item)

            if item.find('#pack=') != -1:
                filename = item.split('#pack=')[-1]
            else:
                filename = item.split('/')[-1].split('#')[0].split('?')[0]

            print "downloading %s..." % item

            remote_file = urllib2.urlopen(item).read()
            local_file = open(os.path.join(path, filename), 'w')
            local_file.close()


    #print js
    #print css