# Getting started with organization-related topics

Here you will find all there is to know about to user management, as well as role management and organization information.

The Organization area contains all the information related to the organization, as well as the management of its members. In this area you will be able to create, manage and delete users, as well as create and assign them different roles in the platform.

##Creating users

You need to be an Owner of the organization to be able to create, manage or delete a user. 

### Web Interface

The Organization view is the first view presented to you after logging in. Just in case you have been navigating around, you only have to click the "Organization" menu option on the left column to go back to it.

> TODO: image

Here, the information we can see depends on the role we have been assigned, and so, if the person logging in is the Owner of the organization...

> TODO: How can I say this without naming the specific role ("Owner")? Which permissions does the user have to have to see the Owner interface?

The different sections are:

- **Organization info card**. Here you can see the most relevant information related to the company: name, type of subscription, and number of members.

- > Question: why is there a "members" list and then a "users" count in the organization info card? Are they different?

- **Subscription**. The subscription plan the company is currently on.

- > Question: here, if we have a subscription fee, does the due date for the payments appear? Maybe it has reminders if you missed a payment?

- **Member list**. Here you can find all the members in your organization, with their name, role and email, and several actions you can do:

  - *Info*: this button shows the member card, and gives us the option of resetting the password and deleting the user.

  - *Edit*: here we can edit the member name, change the password, and edit the role this person has.

  - > Change password: the action should be different in different places:
    >
    > in info, this should be called "reset password" or "send new password", since it should send the user a default password for when they forget or lose it.
    >
    > This is a different functionality than the "change password" in edit, where you enter as the user to change your password (you remember the old one, or you got a default one, and you want to change it).

Under the "Member list" there is an **"Add user"** button. If we click on that, a form appears.

> This should change too: this form should be the sign-up form (with password and confirm password).
>
> Here we should only have: name, email, and the "send new password" button, so the new user gets a default password and has to enter the system and change it. At most, it could have the role too.
>
> I would also change the text of the button "save" to "create user.

By now, the form to sign a user up requires a name, an email, a password and a role. You can save the information, creating a user, or discard it. You can also discard the information by clicking the cross in the upper right corner.

### Public API CLI

Once you log in the system, the command you need is `users`. These are the actions you can take with it:

| add                | info           | list        | reset-password         | update            | del            |
| ------------------ | -------------- | ----------- | ---------------------- | ----------------- | -------------- |
| Creates a new user | Gets user info | Lists users | Resets user's password | Updates user info | Deletes a user |

To create a new user, the command you need would look like this:

```bash
./public-api-cli users add 
	--name=<newuser_name> 
	--password=<newuser_password> 
	--role=<newuser_role> 
	--email=<newuser_email-name>@<email-domain>
```

This command will return a JSON with this structure

```json
{
  "organization_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "email": <newuser_email-name>@<email-domain>,
  "name": <newuser_name>,
  "role_name": <newuser_role>
}
```

where the **email** is the parameter we will use to locate the user in future interactions. For example, if we want to obtain the info related to a specific user, we would need to know their email, like so:

```bash
./public-api-cli users info --email=<email-name>@<email-domain>
```

The response to this command would be the same JSON we received when creating the user, with their current information. If we don't add the `—email`parameter, the info returned would be our own.

## Editing users

There are several operations you can do with the members who belong to your organization, if you're the Owner. 

###Web interface

In the Member list, you can click on the Edit button of the user you want to edit. The following page appears:

> TODO: image

As you can see, the editable fields here are the user's name and role. We can also change the password if we know the current one.

> this option should only be available for the user, who is the only one who knows their current password. 

Once we hit "Save", a notification message appears in the upper right corner of the browser, confirming the changes that have been made.

We can also reset their password, which means we send a default one to the email given when the user was created. To do this, click on the Info button of the user.

> TODO: image

This shows the member card, and on it you can see the "Change password" button. To reset the password, click it.

> TODO: this does NOT send an email with a default password so the user can log in the system. Instead, it opens the "change password" form, for which you need the current password.
>
> Expected behavior: on click, the system sends an email to the user email address with a password, and the only thing we see is a confirmation message in the upper right corner of the screen (like the ones confirming the changes to the user info) saying that the message has been sent.

### Public API CLI

As you don't have an accessible list of users in plain view, the first thing you may want to do is to get one, so you know which users are actually in your organization. To do so, we will use the `users`command again, like so:

```bash
./public-api-cli users list
```

> TODO: responses!!!

To edit a specific user's information, we need their email. With that we can:

- Update their name:

  ```bash
  ./public-api-cli users update --name=<new_name> --email=<email-name>@<email-domain>
  ```

- Update their role:

  ```bash
  ./public-api-cli users update --role_name="Developer" --email=<email-name>@<email-domain>
  ```

- Reset their password (we also need the current password for this):

  ```bash
  ./public-api-cli users reset-password --email=<email-name>@<email-domain> --password=<password> --newPassword=<newpassword>
  ```

>We need to know the response to these commands!

## Deleting users

### Web Interface

 To delete a user, click on the Info button of that user.

> TODO: image

Once in this screen, hit the "Delete user" button. A message will appear on the upper right part of the screen confirming  the action.

### Public API CLI

To delete a user, execute the following command:

```bash
./public-api-cli users del --email=<email-name>@<email-domain>
```

