import requests
import json


class Contactually(object):
    def __init__(self, token, host='https://api.contactually.com'):

        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer %s' % token,
            'Content-type': 'application/json'
        }
        self.host = host

    def _request(self, method, path, data):
        r = method(self.host+path, data=data, headers=self.headers)
        response = json.loads(r.content)
        if response.get('errors'):
            return False, response.get('errors')
        return True, response.get('data')

    def _get_request(self, path, data=None):
        return self._request(requests.get, path, data)

    def _post_request(self, path, data=None):
        return self._request(requests.post, path, data)

    def _patch_request(self, path, data=None):
        return self._request(requests.patch, path, data)

    def _put_request(self, path, data=None):
        return self._request(requests.put, path, data)

    def _delete_request(self, path, data=None):
        return self._request(requests.delete, path, data)

    # ---------------------------------------------------------------- #
    # Authorized User

    def user(self, path='/v2/me'):
        return self._get_request(path)

    def update_user(self, data, path='/v2/me'):
        return self._patch_request(path, data)

    def user_notifications(self, path='/v2/me/notifications'):
        return self._get_request(path)

    def user_prompts(self, path='/v2/me/prompts'):
        """
        Prompts are system-generated via followup rules, programs, or unresponded messages.
        These can only be completed by performing the prescribed action, NOT by this resource's endpoint
        """
        return self._get_request(path)

    def postpone_user_prompt(self, prompt_id, data, path='/v2/me/prompts/%s/postpone'):
        return self._put_request(path % prompt_id, data)

    def user_tasks(self, path='/v2/me/tasks'):
        """
        This endpoint serves as a convenience for retrieving all tasks assigned
        to the current user, however, any edits to those tasks (such as marking
        them completed) occurs via the /v2/tasks/{id} endpoint.
        """
        return self._get_request(path)

    # ---------------------------------------------------------------- #
    # Base Contact

    def list_contacts(self, q='', page=1, path='/v2/contacts'):
        """
        Contacts will be matched via first_name and/or last_name.
        """
        return self._get_request("%s?q=%s&page=%s" % (path, q, page))

    def create_contact(self, data, path='/v2/contacts'):
        """
        Will return existing contact, with all existing data, if email address exists.
        """
        return self._post_request(path, data)

    def fetch_contact(self, contact_id, path='/v2/contacts'):
        return self._get_request("%s/%s" % (path, contact_id))

    def update_contact(self, contact_id, data, path='/v2/contacts'):
        return self._patch_request("%s/%s" % (path, contact_id), data)

    def delete_contact(self, contact_id, path='/v2/contacts'):
        return self._delete_request("%s/%s" % (path, contact_id))

    # Contact Bucket

    def list_contact_buckets(self, contact_id, path='/v2/contacts/%s/buckets'):
        return self._get_request(path % contact_id)

    def add_contact_buckets(self, contact_id, data, path='/v2/contacts/%s/buckets'):
        return self._post_request(path % contact_id, data)

    def update_contact_buckets(self, contact_id, data, path='/v2/contacts/%s/buckets'):
        """
        This endpoint acts like a true PUT and will remove the contact from buckets
        that are not sent, add them to any buckets that are new, and leave the consistent
        bucketing untouched.
        """
        return self._put_request(path % contact_id, data)

    def remove_contact_buckets(self, contact_id, data, path='/v2/contacts/%s/buckets'):
        return self._delete_request(path % contact_id, data)

    # Contact Notes

    def list_contact_notes(self, contact_id, path='/v2/contacts/%s/notes'):
        """
        This endpoint serves as a convenience for retrieving all notes associated
        with the given contact, however, any edits to those notes occurs via the
        /v2/notes/{id} endpoint.
        """
        return self._get_request(path % contact_id)

    # Contact Tasks

    def list_contact_tasks(self, contact_id, path='/v2/contacts/%s/tasks'):
        """
        This endpoint serves as a convenience for retrieving all tasks associated
        with the given contact, however, any edits to those tasks occurs via the
        /v2/tasks/{id} endpoint.
        """
        return self._get_request(path % contact_id)

    # ---------------------------------------------------------------- #
    # Buckets

    def list_buckets(self, q='', path='/v2/buckets'):
        return self._get_request("%s?q=%s" % (path, q))

    def create_bucket(self, data, path='/v2/buckets'):
        return self._post_request(path, data)

    def fetch_bucket(self, bucket_id, path='/v2/buckets'):
        return self._get_request("%s?id=%s" % (path, bucket_id))

    def update_bucket(self, bucket_id, data, path='/v2/buckets'):
        return self._patch_request("%s?id=%s" % (path, bucket_id), data)

    def delete_bucket(self, bucket_id, path='/v2/buckets'):
        return self._delete_request("%s?id=%s" % (path, bucket_id))

    # Bucket Contacts

    def list_bucket_contacts(self, bucket_id, path='/v2/buckets/%s/contacts'):
        return self._get_request(path % bucket_id)

    def add_bucket_contacts(self, bucket_id, data, path='/v2/buckets/%s/contacts'):
        return self._post_request(path % bucket_id, data)

    def remove_bucket_contacts(self, bucket_id, data, path='/v2/buckets/%s/contacts'):
        return self._delete_request(path % bucket_id, data)

    # ---------------------------------------------------------------- #
    # Tasks

    def create_task(self, data, path='/v2/tasks'):
        return self._post_request(path, data)

    def fetch_task(self, task_id, path='/v2/tasks'):
        return self._get_request("%s?id=%s" % (path, task_id))

    def update_task(self, task_id, data, path='/v2/tasks'):
        return self._patch_request("%s?id=%s" % (path, task_id), data)

    def delete_task(self, task_id, path='/v2/tasks'):
        return self._delete_request("%s?id=%s" % (path, task_id))

    def mark_task_complete(self, task_id, path='/v2/tasks/%s/complete'):
        return self._post_request("%s?id=%s" % (path, task_id))

    def mark_task_incomplete(self, task_id, path='/v2/tasks/%s/complete'):
        return self._delete_request("%s?id=%s" % (path, task_id))
