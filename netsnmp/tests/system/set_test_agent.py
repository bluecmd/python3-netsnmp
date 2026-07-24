import sys


ROOT = '.1.3.6.1.4.1.8072.9999.9999'
INTEGER_OID = ROOT + '.1.0'
VALUES = {
    INTEGER_OID: ('integer', '42'),
}


def respond(*lines):
    print(*lines, sep='\n', flush=True)


for command in sys.stdin:
    command = command.rstrip('\n')
    if command == 'PING':
        respond('PONG')
    elif command == 'get':
        oid = sys.stdin.readline().rstrip('\n')
        value = VALUES.get(oid)
        if value is None:
            respond('NONE')
        else:
            respond(oid, value[0], value[1])
    elif command == 'set':
        oid = sys.stdin.readline().rstrip('\n')
        value_type, value = sys.stdin.readline().rstrip('\n').split(' ', 1)
        if oid not in VALUES:
            respond('not-writable')
        else:
            VALUES[oid] = (value_type, value)
            respond('DONE')
    else:
        respond('NONE')
