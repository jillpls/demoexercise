class Campaign(object):
    video_id = 0
    template_id = 0 
    contact_list_id = 0 

    def __init__(self, video_id, template_id, contact_list_id):
        self.video_id = video_id
        self.template_id = template_id
        self.contact_list_id = contact_list_id

    def __str__(self) -> str:
        return f'[video_id:{self.video_id}, template_id:{self.template_id}, contact_list_id:{self.contact_list_id}]'