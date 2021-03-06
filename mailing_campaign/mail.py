"""Contains classes and helper functions to handle a mail campaign POST
Classes in this module are not Models and cannot be stored in the database
"""
from typing import List
from mailing_campaign.models import Contact, Video


class Campaign(object):
    """Class for receiving and processing an email campaign POST
    """
    video_id = 0
    template_id = 0
    contact_list_id = 0
    contact_list = None
    video: Video = None

    def __init__(self, video_id, template_id, contact_list_id):
        self.video_id = video_id
        self.template_id = template_id
        self.contact_list_id = contact_list_id

    def __str__(self) -> str:
        return (
            f"[video_id:{self.video_id}, template_id:{self.template_id}, "
            f"contact_list_id:{self.contact_list_id}] "
        )


class MailData(object):
    """Content of an email sent through a CampaignPost
    """
    first_name = ""
    last_name = ""
    video_link = ""

    def __init__(self, first_name, last_name, video_link):
        self.first_name = first_name
        self.last_name = last_name
        self.video_link = video_link


class Mail(object):
    """Email sent through a CampaignPost
    """
    email_address = ""
    data = None

    def __init__(self, email_address, data):
        self.email_address = email_address
        self.data = data


class CampaignPost(object):
    """Class used for re-serialization of a received Campaign
    """
    template_id = 0
    instances = None

    def __init__(self, template_id, instances=[]):
        self.template_id = template_id
        self.instances = instances


def generate_instances(campaign: Campaign) -> List[Mail]:
    """Generates a list of Mail objects from a campaign

    Args:
        campaign (Campaign): source Campaign

    Raises:
        ValueError: if a campaign field is None

    Returns:
        List[Mail]: list of Mail objects
    """
    if campaign.contact_list is None:
        raise ValueError("campaign.contact_list may not be None")
    if campaign.video is None:
        raise ValueError("campaign.video not be None")

    contacts = Contact.objects.filter(contact_list=campaign.contact_list)
    video_link = campaign.video.link

    mails = []

    for contact in contacts:
        mail_data = MailData(contact.first_name, contact.last_name, video_link)
        mail = Mail(contact.email_address, mail_data)
        mails.append(mail)

    return mails
