from pymavlink.dialects.v20 import ardupilotmega as mavlink
from io import BytesIO


def test_protocol(mavlink, signing=False):
    # we will use a fifo as an encode/decode buffer
    f = BytesIO()

    # create a mavlink instance, which will do IO on file object 'f'
    mav = mavlink.MAVLink(f)

    if signing:
        mav.signing.secret_key = chr(42) * 32
        mav.signing.link_id = 0
        mav.signing.timestamp = 0
        mav.signing.sign_outgoing = True

    # set the WP_RADIUS parameter on the MAV at the end of the link
    mav.param_set_send(7, 1, bytearray(b"WP_RADIUS"), 101, mavlink.MAV_PARAM_TYPE_REAL32)

    # alternatively, produce a MAVLink_param_set object
    # this can be sent via your own transport if you like
    m = mav.param_set_encode(7, 1, bytearray(b"WP_RADIUS"), 101, mavlink.MAV_PARAM_TYPE_REAL32)

    m.pack(mav)

    # get the encoded message as a buffer
    b = m.get_msgbuf()

    bi = []
    for c in b:
        bi.append(int(c))
    print(bi)

    # decode an incoming message
    m2 = mav.decode(b)

    # show what fields it has
    print("Got a message with id %u and fields %s" % (m2.get_msgId(), m2.get_fieldnames()))

    # print out the fields
    print(m2)


print("Testing mavlink2")
test_protocol(mavlink)
print()
# print("Testing mavlink2 with signing")
# test_protocol(mavlink, True)