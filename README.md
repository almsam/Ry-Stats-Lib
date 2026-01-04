# Ry Statistics Language

## Project Description:

Ry is a modern statistical computing system inspired by R, built on a Python-native core.

The project has two tightly aligned use cases:

1. A modern R like statistical programming language with its own interpreter, powered by a Python backend, and that will hopefully be as easy to use as R but with better syntax
2. A Python statistics library that provides a clean interface for all the relevant statistical functions and data structures

These two use cases should utilize the same backend of statistical functions, allowing consistency across the Python API and the Ry language

As an ambitious long term goal, Ry aims to have the advantage of R's ease of use for initial exploration and prototyping, while also providing a smooth transition path to production level code in Python. The team currently thinks this can be achieved by having a script in place similar to an interpreter to convert a .Ry file to a .py file, leveraging the shared backend and consistent syntax and semantics between Ry and Python

## Software Licence:

``` {text}
OSPREY License

Copyright (c) 2025-2026 Samira
Developed under the OSPREY Project (Open Source Projects for Research, Education, & You)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. **Attribution**  
   The above copyright notice, this license, and the following attribution notice
   shall be included in all copies or substantial portions of the Software:

   > "This software is part of the OSPREY Project (https://github.com/almsam/OSPREY),  
   > created by contributors including
	["Samira"
	  or "Almsam"
	  or "https://github.com/almsam"].  
   > For more information, visit:
   >> https://github.com/almsam/OSPREY & 
   >> https://github.com/almsam/OSPREY/Social Code of Conduct.md "

2. **Community Respect Clause**  
   The Software shall not be used in any project or system that violates the OSPREY Social Code of Conduct
	> For more information, see(https://github.com/almsam/OSPREY/Social code of conduct.md).  
   This includes but is not limited to projects or applications that promote hate, discrimination (racism,
   sexism, homophobia, transphobia, or abelism), or harassment of any kind.

3. **Educational and Collaborative Spirit**  
   Users are encouraged, though not required, to contribute improvements back to the OSPREY community  
   to support its educational and mentoring mission. Contributions may be made through pull requests  
   or other collaboration tools on GitHub.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```