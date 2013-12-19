from sllurp.message import SllurpMessage, SllurpMessageParameter

class AccessSpecParameter (SllurpMessageParameter):
    msg_type = 0 # XXX

# XXX figure out where this goes
class LLRPStatusParameter (SllurpMessageParameter):
    msg_type = 0 # XXX

# 16.1.17 ADD_ACCESSSPEC
class ADD_ACCESSSPEC (SllurpMessage):
    msg_type = 40
    fields = SllurpMessage.fields + ( \
        ('AccessSpec', AccessSpecParameter))

# 16.1.18 ADD_ACCESSSPEC_RESPONSE
class ADD_ACCESSSPEC_RESPONSE (SllurpMessage):
    msg_type = 50
    fields = SllurpMessage.fields + ( \
        ('LLRPStatus', LLRPStatusParameter))

# 16.1.19 DELETE_ACCESSSPEC
class DELETE_ACCESSSPEC (SllurpMessage):
    msg_type = 41
    fields = SllurpMessage.fields + ( \
        ('AccessSpecID', '!I'))

# 16.1.20 DELETE_ACCESSSPEC_RESPONSE
class DELETE_ACCESSSPEC_RESPONSE (SllurpMessage):
    msg_type = 51
    fields = SllurpMessage.fields + ( \
        ('LLRPStatus', LLRPStatusParameter))

# 16.1.21 ENABLE_ACCESSSPEC
class ENABLE_ACCESSSPEC (SllurpMessage):
    msg_type = 42
    fields = SllurpMessage.fields + ( \
        ('AccessSpecID', '!I'))

# 16.1.22 ENABLE_ACCESSSPEC_RESPONSE
class DELETE_ACCESSSPEC_RESPONSE (SllurpMessage):
    msg_type = 51
    fields = SllurpMessage.fields + ( \
        ('LLRPStatus', LLRPStatusParameter))

# 16.1.23 DISABLE_ACCESSSPEC
class DISABLE_ACCESSSPEC (SllurpMessage):
    msg_type = 43
    fields = SllurpMessage.fields + ( \
        ('AccessSpecID', '!I'))

# 16.1.24 DISABLE_ACCESSSPEC_RESPONSE
class DISABLE_ACCESSSPEC_RESPONSE (SllurpMessage):
    msg_type = 53
    fields = SllurpMessage.fields + ( \
        ('LLRPStatus', LLRPStatusParameter))

# 16.1.25 GET_ACCESSSPECS
class DISABLE_ACCESSSPEC (SllurpMessage):
    msg_type = 44
    fields = SllurpMessage.fields

# 16.1.26 GET_ACCESSSPECS_RESPONSE
class GET_ACCESSSPECS_RESPONSE (SllurpMessage):
    msg_type = 54
    fields = SllurpMessage.fields + ( \
        ('LLRPStatus', LLRPStatusParameter),
        ('AccessSpec', AccessSpecParameter, 0))
