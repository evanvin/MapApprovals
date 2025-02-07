import os
import logging
from Functions.Shared import (
    getUnapprovedCount,
    postMessageToMapChannel
)

def handleCheckUnapprovedTrigger() -> None:
    logging.info('Handline Check Unapproved.')
    unapprovedUpdateCount = getUnapprovedCount(os.getenv('GRAVITY_FORM_WORKOUT_FORM_ID'))
    unapprovedDeleteCount = getUnapprovedCount(os.getenv('GRAVITY_FORM_DELETE_FORM_ID'))

    if unapprovedUpdateCount == 0 & unapprovedDeleteCount == 0:
        logging.info('No unapproved.')
        return
    
    message = []
    if unapprovedUpdateCount > 0:
        message.append(str(unapprovedUpdateCount) + ' updates')
    if unapprovedDeleteCount > 0:
        message.append(str(unapprovedDeleteCount) + ' deletes')
    
    postMessageToMapChannel(text='<!channel>, there are unapproved requests: ' + ', '.join(message) + '. <' + os.getenv('GRAVITY_FORMS_BASE_URL') + '/wp-admin/admin.php?page=gf_entries&filter=gv_unapproved&id=' + os.getenv('GRAVITY_FORM_WORKOUT_FORM_ID') + '|Link>')
    logging.info('Sent unapproved counts to Slack. Done handling.')