name: Bug Report
description: Create a report to help us fix a bug or unexpected behavior.
title: "[BUG] "
labels: ["bug"]
assignees: ["sedmugen"]
body:
  - type: markdown
    attributes:
      value: Thank you for taking the time to report an issue!
  - type: textarea
    id: description
    attributes:
      label: Describe the Bug
      description: Provide a clear and concise description of what the bug is.
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Describe how to reproduce the behavior step-by-step.
      placeholder: |
        1. Run './start.sh'
        2. Execute 'curl http://localhost/api/items'
        3. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: Describe what you expected to happen.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment Details
      description: Include OS version, Docker version, Minikube version, etc.
      placeholder: "OS: Windows 11 / Ubuntu 22.04 | Docker: 24.0.5 | Minikube: v1.32"
    validations:
      required: false
