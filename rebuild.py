'''
Removes container, removes image, builds image, starts container
Fill in the required image/container tag/name and any args
All containers use 'docker run' with '--name [CONTAINER]'
Script assumes Dockerfile at .
'''

from os import system

def sprint(string, color):
    '''Tries to print with termcolor.cprint'''
    try:
        from termcolor import cprint
        printer = 'col'
    except ModuleNotFoundError:
        printer = 'nocol'
    if printer == 'col':
        cprint(string, color)
    elif printer == 'nocol':
        print(string)

def spacer(string):
    '''Tests and modifies spaces in *_args'''
    if string == '':
        return ''
    if string[len(string)-1] == ' ':
        return string
    string = string + ' '
    return string

def remake(container, build_args, start_args):
    '''Remove container and image, build image and start container CONTAINER'''
    build_args = spacer(build_args)
    start_args = spacer(start_args)

    remove_container = 'docker rm '+container
    remove_image = 'docker rmi '+container
    build_image = 'docker build '+build_args+'-t '+container+' .'
    start_container = 'docker run --name '+container+' '+start_args+container

    sprint(remove_container, 'yellow')
    system(remove_container)
    sprint(remove_image, 'yellow')
    system(remove_image)
    sprint(build_image, 'yellow')
    system(build_image)
    sprint(start_container, 'yellow')
    system(start_container)

if __name__ == '__main__':
    CONTAINER = 'kiosk-server'
    BUILD_ARGS = ''
    START_ARGS = '-p 80:80'
    remake(CONTAINER, BUILD_ARGS, START_ARGS)
