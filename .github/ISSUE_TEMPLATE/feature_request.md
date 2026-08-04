name: Feature Request
description: Suggest an idea or feature enhancement for this project.
title: "[FEAT] "
labels: ["enhancement"]
assignees: ["sedmugen"]
body:
  - type: markdown
    attributes:
      value: Have a feature suggestion? Let us know!
  - type: textarea
    id: feature-description
    attributes:
      label: Feature Description
      description: Is your feature request related to a problem or a new capability?
    validations:
      required: true
  - type: textarea
    id: proposed-solution
    attributes:
      label: Proposed Solution
      description: Describe the solution or workflow you would like to see implemented.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Describe any alternative solutions or features you have considered.
    validations:
      required: false
