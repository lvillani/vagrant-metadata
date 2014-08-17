# Contributing

Our community welcomes contributions of every kind: documentation, code, artwork, any help is
greatly appreciated. Since we all have limited time at our disposal, this document contains all
sorts of informations and guidelines about how to contribute and interact with us.


## Contributing Code

This project keeps its source code on [GitHub](https://www.github.com/) and takes contributions
through [GitHub pull requests](https://help.github.com/articles/using-pull-requests). For smaller
contributions and bug fixes just go ahead and either report an issue or submit a pull request. It
is usually a good idea to discuss major changes with developers, to avoid duplicated efforts and
determine whether your contribution would be a good fit for the project and it is likely to be
accepted. There's nothing worse than seeing your hard work being rejected because it falls
outside of the scope of the project.

Make sure your editor respects the [EditorConfig](http://editorconfig.org/) configuration file we
put at the root of the repository.

We follow [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html) as our git workflow of
choice which boils down to:

* The `master` branch is always stable and deployable.
* To work on something new, branch off `master` and give the new branch a descriptive name (e.g.:
  `sort-packages-by-name`, `issue-32`).
* Regularly __rebase__ that branch against `master` and push your work to a branch with the same
  name on the server.
* When you need feedback, help or think you are ready,
  [submit a pull request](https://help.github.com/articles/using-pull-requests).
* Once the branch has been merged (or rebased) into `master`, delete it from both your local and
  remote repository.

We invite you to follow
[these guidelines](http://who-t.blogspot.de/2009/12/on-commit-messages.html) to write useful
commit messages.

Additionally, you don't need to add entries to the [CHANGELOG.md](CHANGELOG.md) file, that is a
responsibility of the project's maintainers.


## Reading List

* [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html)
* [Keep a Changelog](http://keepachangelog.com/)
* [On Commit Messages](http://who-t.blogspot.de/2009/12/on-commit-messages.html)
* [Semantic Versioning](http://semver.org/)
