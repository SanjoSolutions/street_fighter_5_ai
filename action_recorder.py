# bitmap:
# (
#   UP PRESS,
#   UP RELEASE,
#   LEFT PRESS,
#   LEFT RELEASE,
#   DOWN PRESS,
#   DOWN RELEASE,
#   RIGHT PRESS,
#   RIGHT RELEASE,
#   LP PRESS,
#   LP RELEASE,
#   MP PRESS,
#   MP RELEASE,
#   HP PRESS,
#   HP RELEASE,
#   LMHP PRESS,
#   LMHP RELEASE,
#   LK PRESS,
#   LK RELEASE,
#   MK PRESS,
#   MP RELEASE,
#   HK PRESS,
#   HK RELEASE,
#   LMHP PRESS,
#   LMHP RELEASE,
# )

from inputs import get_gamepad


def event_to_entry(event):
    return (event.timestamp, event.code, event.state)


with open('actions_3.txt', 'a') as file:
    while True:
        events = get_gamepad()
        for event in events:
            if (
                event.ev_type == 'Key' or
                (
                    event.ev_type == 'Absolute' and
                    event.code in {'ABS_HAT0X', 'ABS_HAT0Y', 'ABS_RZ', 'ABS_Z'}
                )
            ):
                entry = event_to_entry(event)
                file.write(str(entry) + '\n')
                file.flush()
