# Sara's maternity leave

Hi! I'm Sara, and if you're reading this I'm probably sleeping too little and taking care of an unbelievably small human being. And you have been assigned the management of Nalej's documentation! Congratulations!

Your main mission is to translate the technical specifications of the features that the team develops at frightening speed into human-readable documents, so the future users of the platform know how to navigate their way through it.

## About the documentation

Ok, the first thing you need to know is that the documentation is displayed in GitBook, which is synchronized with the GitHub documentation repository. The documents are in Markdown (`.md`), and you can see the Nalej documentation interface in GitBook [here](https://app.gitbook.com/@nalej/s/docs/).

So, what do you need?

- the `public-api-cli`, to test what you're documenting.
- access to one of the latest web interfaces, for the same reason (this changes like three times a week, so just ask out in the open where can you connect to test whatever, and someone, probably Gaizka, will answer and send you the credentials to connect).
- a Markdown editor (I personally use Typora to edit them, since I find it quite comfortable).

You should check with Alvaro or Dani whether you have access to GitBook and the GitHub repo, since you will be uploading the changes there. When access is granted, download the repo in your computer and you can start editing!

### File structure

When you download the repo you will have the following structure:

```
README.md
SUMMARY.md
|_ .git
|_ .gitbook
	|_ assets
|_ organization
|_ infrastructure
|_ devices
|_ applications
|_ tutorials

```

The viewable folders are the ones that contain the documents, classified by platform component (each folder is a section of the web interface, to make it easier to browse through it).

The documentation interface has a column on the left part of the screen. This column has links to all the documents, and to include a new document there you have to edit the `SUMMARY.md` file and link to it from there.

The `README.md` is the landing page, so you have to edit it if you want to see changes there.

### Images

The images are included in the `.gitbook/assets` folder. The path of the images must be relative when including them in a document, for example:

```
![generic image] (../../generic_image.png)
```

If you copy a section of a document with an image in it and paste it afterwards, the image path may have changed to an absolute one, referencing the file in your computer. Check this out before uploading the document, because in this case the image will appear as a broken link.

## Creating docs for a new release

To create a new release you have to create a new branch in GitHub. Call this branch the name of the *current* release, not the new one, because the new one will be the master branch.

After that, GitBook should update by itself, with a new branch called "master". To change the branch name you just need to go into **edit mode** (clicking on the pencil icon in the lower right corner) and change the name of the branch there. The releases 0.2.0 and 0.3.0 are already created, and the 0.4.0 is the one we're currently working with.

Once this is done, you should be able to upload the new changes to the master branch, and expect them to appear under the new version of the documentation.

## Who to ask

Chances are, you already know this. In case you don't, here is a helpful guide of who's who in Daisho.

Dani and Álvaro are the default people to ask. They will answer you quickly, and if they can't they will redirect you to someone who can. The only problem is that they are often unavailable.

Rodrigo is in charge of DevOps & QA. If you have problems with anything technical that you're afraid to ask (think of questions that may get you look like an idiot), first Google it, and then ask him, he will gladly help. He's also the expert of the Edge Controllers and the Agents so, for questions about that, go directly to him.

Carmen and Gaizka are the backend developers, with Dani as their lead. I would suggest asking Dani first, so he can redirect you to the person who can answer better.

Juanma is developing the cluster management part, so for questions about that, he will be the best choice.

And last, but not least, Iván and Blanca are the front-end developers, so they know the web interface inside and out. Anything about it, they are the ones to ask.

Don't be afraid to ask. The team is warm and welcoming, and they will be happy to help. 

Welcome aboard!