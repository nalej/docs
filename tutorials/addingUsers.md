# Adding users to the system

As a system owner, you probably have to add new users to the system. First we need to explain the different roles that are available in the system, and then how to assign them to new users.

## System roles

There are three default roles in the system.

- **Owner**: has almighty powers in the system. They can add, modify and delete users, applications, devices...
- **Developer**:
- **Operator**:

> should we say that these are the default roles and we can create our own? is it possible within the system as it is now, or the users have to stick to these roles by now?

Now that you know about the roles, let's see how the users are created in the system.

## Creating users

### Web Interface

In the Organization view, under the "Member list" there is an **"Add user"** button. If we click on that, a form appears.

!["Add user" feature view](/Users/svillanueva/nalej_docs/docs/.gitbook/assets/org_add_user.png)

By now, the form to sign a user up requires a name, an email, a password and a role. You can save the information (thus creating a user) or discard it. You can also discard the information by clicking the cross in the upper right corner.

### Public API CLI

Once you log in the system, the command you need is `users`.  To create a new user, the command you need would look like this:

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
  "organization_id": <org_id>,
  "email": <newuser_email-name>@<email-domain>,
  "name": <newuser_name>,
  "role_name": <newuser_role>
}
```

where the **role_name** is one of the roles we saw in the first section of this document, and the **email** is the parameter we will use to locate the user in future interactions. For example, if we want to obtain the info related to a specific user, we would need to know their email, like so:

```bash
./public-api-cli users info 
	--email=<email-name>@<email-domain>
```

The response to this command would be the same JSON we received when creating the user, with their current information. If we don't add the `--email` parameter, the info returned would be our own.

For more information on how to manage and delete users, please go to [this document](../organization/organization-1.md), where those situations are explained in depth.