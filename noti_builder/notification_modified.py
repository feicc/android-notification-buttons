from jnius import autoclass
from plyer.platforms.android import activity, SDK_INT

def return_intent(intentName):
    intent = Intent(intentName)
    return intent

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
aString = autoclass('java.lang.String')
aInt = autoclass('java.lang.Integer')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
PythonService = autoclass('org.renpy.android.PythonService')
Pend = autoclass('android.app.PendingIntent')
this = PythonService.mService
if SDK_INT > 22:
    Action_Builder = autoclass('android.app.Notification$Action$Builder')

class AndroidNotification:
    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def notify(self, **kwargs):
        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))
        noti = NotificationBuilder(activity)

        ## Icon integers are available at https://developer.android.com/reference/android/R.drawable.html
        if SDK_INT >= 16:
            for bAction,bName,bIcon,bCallback in kwargs['buttons']:
                intent = return_intent(kwargs['intentName']+bAction)
                pend = Pend.getBroadcast( this, 100, intent, 0)
                if SDK_INT < 23:
                    noti.addAction(bIcon, aString(bName), pend)

                else:
                    action = Action_Builder(bIcon, aString(bName), pend)
                    action = action.build()
                    noti.addAction(action)

        noti.setContentTitle(aString( kwargs.get('title').encode('utf-8')))
        noti.setContentText(aString( kwargs.get('message').encode('utf-8')))
        noti.setTicker(aString( kwargs.get('ticker').encode('utf-8')))

        noti.setSmallIcon(icon)
        noti.setAutoCancel(True)

        if SDK_INT >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(kwargs['num'], noti)


def instance():
    return AndroidNotification()
