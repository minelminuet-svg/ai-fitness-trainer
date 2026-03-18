# Contributing to AI Fitness Trainer

First off, thank you for considering contributing to AI Fitness Trainer! It's people like you that make this such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **the expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* End all files with a newline
* Document new code based on the Documentation Styleguide

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use type hints for function signatures
* Write docstrings for all modules, classes, and functions
* Use meaningful variable names
* Max line length: 100 characters

Example:

```python
def process_landmarks(landmarks: Dict[str, LandmarkPoint], 
                     reference_point: LandmarkPoint) -> Dict[str, LandmarkPoint]:
    """
    Normalize landmarks relative to a reference point.
    
    Args:
        landmarks: Dictionary of detected landmarks
        reference_point: Reference point for normalization
        
    Returns:
        Dictionary of normalized landmarks
    """
    # Implementation
```

### Documentation Styleguide

* Use Markdown
* Reference function names in backticks
* Include code examples where relevant
* Keep sentences clear and concise

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment
3. Install development dependencies: `pip install -r fitness_trainer/requirements.txt`
4. Create a new branch for your work
5. Make your changes
6. Run tests before pushing
7. Push to your fork and submit a pull request

## Testing

Please write tests for new features. Run tests with:

```bash
pytest tests/ -v
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested

---

Thank you for contributing! 🎉
