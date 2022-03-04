# Contribution Guidelines

Welcome to the *dicom_parser* repository! We're excited you're here and want to contribute.

These guidelines are designed to make it as easy as possible to get involved. If you have any questions that aren't discussed below, please let us know by opening an [issue][link_issues]!

Before you start you'll need to set up a free [GitHub][link_github] account and sign in. Here are some [instructions][link_signupinstructions].

Already know what you're looking for in this guide? Jump to the following sections:
- [Contribution Guidelines](#contribution-guidelines)
  - [Issue labels](#issue-labels)
  - [Making a change](#making-a-change)
  - [Notes for New Code](#notes-for-new-code)
      - [Testing](#testing)
  - [Recognizing Contributions](#recognizing-contributions)
  - [Thank you!](#thank-you)

## Issue labels

The current list of issue labels are [here][link_labels] and include:

* [![Bugs](https://img.shields.io/badge/-bugs-fc2929.svg)][link_bugs] *These issues point to problems in the project.*

    If you find a new bug, please provide as much information as possible to recreate the error.
    The [issue template][link_issue_template] will automatically populate any new issue you open, and contains information we've found to be helpful in addressing bug reports.
    Please fill it out to the best of your ability!

    If you experience the same bug as one already listed in an open issue, please add any additional information that you have as a comment.

* [![Help Wanted](https://img.shields.io/badge/-help%20wanted-c2e0c6.svg)][link_helpwanted] *These issues contain a task that a member of the team has determined we need additional help with.*

    If you feel that you can contribute to one of these issues, we especially encourage you to do so!
    Issues that are also labelled as [good-first-issue][link_good_first_issue] are a great place to start if you're looking to make your first contribution.

* [![Enhancement](https://img.shields.io/badge/-enhancement-00FF09.svg)][link_enhancement] *These issues are asking for new features to be added to the project.*

    Please try to make sure that your requested enhancement is distinct from any others that have already been requested or implemented.
    If you find one that's similar, but there are subtle differences, please reference the other request in your issue.

## Making a change

We appreciate all contributions to *dicom_parser*, but those accepted fastest will follow a workflow similar to the following:

**1. Comment on an existing issue or open a new issue referencing your addition.**

This allows other members of the *dicom_parser* development team to confirm that you aren't overlapping with work that's currently underway and that everyone is on the same page with the goal of the work you're going to carry out.

[This blog][link_pushpullblog] is a nice explanation of why putting this work in up front is so useful to everyone involved.

**2. [Fork][link_fork] the [*dicom_parser* repository][link_rep] to your profile.**

This is now your own unique copy of the *dicom_parser* repository.
Changes here won't affect anyone else's work, so it's a safe space to explore edits to the code!

You can clone your *dicom_parser* repository in order to create a local copy of the code on your machine. To install your version of *dicom_parser*, and the dependencies needed for development, in your Python environment, run `pip install -e ".[dev]"` from your local *dicom_parser* directory.

Make sure to keep your fork up to date with the original *dicom_parser* repository. One way to do this is to [configure a new remote named "upstream"](https://help.github.com/articles/configuring-a-remote-for-a-fork/) and to [sync your fork with the upstream repository][link_updateupstreamwiki].

**3. Make the changes you've discussed.**

When you are working on your changes, test frequently to ensure you are not breaking the existing code.
For more on testing, please see [the testing section of *dicom_parser* README](https://github.com/open-dicom/dicom_parser#tests).

It's a good practice to create [a new branch](https://help.github.com/articles/about-branches/) of the repository for a new set of changes.

**4. Submit a [pull request][link_pullrequest].**

A new pull request for your changes should be created from your fork of the repository.

**5. Install pre-commit.**

[pre-commit](https://pre-commit.com/) is a git hook for running operations at commit time. To use it in your environment, do `pip install pre-commit` following by `pre-commit install` inside your source directory.

Pull requests should be submitted early and often (please don't mix too many unrelated changes within one PR)!
If your pull request is not yet ready to be merged, please also include the **[WIP]** prefix (you can remove it once your PR is ready to be merged) or label it is a "draft". This tells the development team that your pull request is a "work-in-progress", and that you plan to continue working on it.

Review and discussion on new code can begin well before the work is complete, and the more discussion the better! The development team may prefer a different path than you've outlined, so it's better to discuss it and get approval at the early stage of your work.

One your PR is ready a member of the development team will review your changes to confirm that they can be merged into the main codebase.

## Notes for New Code

#### Testing
New code should be tested, whenever feasible. Bug fixes should include an example that exposes the issue. Any new features should have tests that show at least a minimal example. If you're not sure what this means for your code, please ask in your pull request.

## Recognizing Contributions

We welcome and recognize all contributions from documentation to testing to code development.

The development team member who accepts/merges your pull request will update the CHANGES file to reference your contribution.

You can see a list of current contributors in our [zenodo file][link_zenodo]. If you are new to the project, don't forget to add your name and affiliation there!

## Thank you!

You're awesome. :wave::smiley:

<br>

*&mdash; Based on contribution guidelines from the [nipype][link_nipype] project.*

[link_github]: https://github.com/
[link_rep]: https://github.com/open-dicom/dicom_parser
[link_signupinstructions]: https://help.github.com/articles/signing-up-for-a-new-github-account
[link_react]: https://github.com/blog/2119-add-reactions-to-pull-requests-issues-and-comments
[link_issues]: https://github.com/open-dicom/dicom_parser/issues
[link_labels]: https://github.com/open-dicom/dicom_parser/labels
[link_discussingissues]: https://help.github.com/articles/discussing-projects-in-issues-and-pull-requests
[link_bugs]: https://github.com/open-dicom/dicom_parser/labels/bug
[link_issue_template]: https://github.com/open-dicom/dicom_parser/blob/master/.github/ISSUE_TEMPLATE/feature_request.md
[link_helpwanted]: https://github.com/open-dicom/dicom_parser/labels/help-wanted
[link_good_first_issue]: https://github.com/open-dicom/dicom_parser/issues?q=is%3Aopen+is%3Aissue+label%3Agood-first-issue
[link_enhancement]: https://github.com/open-dicom/dicom_parser/labels/enhancement
[link_orphaned]: https://github.com/open-dicom/dicom_parser/pulls?q=is%3Apr+label%3Aorphaned+is%3Aclosed
[link_pullrequest]: https://help.github.com/articles/creating-a-pull-request-from-a-fork/
[link_fork]: https://help.github.com/articles/fork-a-repo/
[link_pushpullblog]: https://www.igvita.com/2011/12/19/dont-push-your-pull-requests/
[link_updateupstreamwiki]: https://help.github.com/articles/syncing-a-fork/
[link_new_interfaces]: http://nipype.readthedocs.io/en/latest/devel/interface_specs.html
[link_cloning]: https://help.github.com/articles/cloning-a-repository/
[link_nipype]: https://github.com/nipy/nipype
[link_zenodo]: https://github.com/open-dicom/dicom_parser/blob/master/.zenodo.json
