import struct

class EncodingError (Exception):
    pass

class DecodingError (Exception):
    pass

class SllurpMessage (object):
    msg_type = None
    message_id = 0

    fields = (
        # (name, struct fmt, start bit index, length (bits), optional, multiple)
        ('MessageType',     '!H', 6, 10, False, False),
        ('MessageLength',   '!I', 0, 32, False, False),
        ('MessageID',       '!I', 0, 32, False, False),
    )

    def __init__ (self, msg_dict=None, bytestr=None):
        """
        Arguments:
            msg_dict: A dictionary of field values.  Must contain values for all
                fields except for MessageLength, MessageType, and MessageID, all
                of which self.encode() will fill in automatically.

        For fields that have their own encoding schemes defined, e.g., command
        parameters, pass an instance of a class that subclasses SllurpMessage.

        Example for an ADD_ACCESSSPEC command:

            # ACCESS_SPEC is a subclass of SllurpMessage
            access_spec = ACCESS_SPEC(...)

            # ADD_ACCESSSPEC is also a subclass of SllurpMessage
            add_accessspec = ADD_ACCESSSPEC({'AccessSpec': access_spec})
            as_bytes = add_accessspec.encode()
        """
        assert (bool(msg_dict is not None) ^ bool(bytestr is not None))
        self.msg_dict = msg_dict
        self.bytestr = bytestr

    def encode (self):
        """Returns the binary LLRP representation of this SllurpMessage.
        Automatically fills the MessageLength, MessageType, and MessageID
        fields."""

        data = ''

        # fill MessageID field
        self.msg_dict['MessageID'] = SllurpMessage.next_message_id()
        self.msg_dict['MessageType'] = self.msg_type
        self.msg_dict['MessageLength'] = 0 # will be computed last

        len_field_pos = None

        # iterate through all fields in the message type, building up the data
        # string one field at a time
        for fname, fmt, bit_index, len_bits, optional, multiple in self.fields:
            # save the position of the MessageLength field to patch up later
            if fname == 'MessageLength':
                len_field_pos = len(data)
            try:
                value = self.msg_dict[fname]
            except KeyError:
                if optional:
                    continue # skip this field
                raise EncodingError('Required field {} is ' \
                        'missing'.format(fname))
            if multiple and isinstance(value, (list, tuple)):
                values = value
            else:
                values = (value,)
            for val in values:
                fieldwidth_bits = 8 * struct.calcsize(fmt)
                assert(len_bits <= fieldwidth_bits)
                shiftwidth = fieldwidth_bits - bit_index - len_bits
                if isinstance(val, int) and shiftwidth:
                    val <<= shiftwidth
                data += struct.pack(fmt, val)

        # patch up MessageLength field with the final length
        assert (len_field_pos is not None)
        data = data[ : len_field_pos] + struct.pack('!I', len(data)) + \
            data[len_field_pos + struct.calcsize('!I') : ]

        return data

    def decode (self, bytestr):
        # TODO: write me
        return {}

    @classmethod
    def next_message_id (_):
        SllurpMessage.message_id += 1
        return SllurpMessage.message_id

class SllurpMessageParameter (SllurpMessage):
    # XXX
    pass
