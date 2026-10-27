# Reflection

Swaroop Venkateshwar - PES1UG24CS923

**1. Which issues were the easiest and which were the hardest to fix?**

Flake8 ones were the easiest, it's just blank lines and splitting long lines, and docstrings/renaming from Pylint were also easy. The hardest was the pickle one, because I couldn't just delete it. I had to change the backup to json and then I noticed that json makes the order ids strings, so after restore the keys didn't match anymore. I had to convert them back to int. Removing the `global next_id` was also a bit tricky because then I had to think of another way to get new ids.

**2. Did the tools give any false positives?**

Not really false positives, but some of the messages were not very useful. The missing docstring warnings (C0116) were everywhere and don't change how the program works. Bandit's B403 on just `import pickle` is a "Low" warning and kind of repeats the B301 one. On the other side, the tools did not catch some real bugs - unknown dishes costing 99, "teleported" being accepted as a status, and the empty order. I only found those by running the program and reading the output, so the tools can't replace testing.

**3. How would you integrate static analysis into your development workflow?**

I would run flake8 and pylint in the editor (VS Code shows them as I type) and add them as a pre-commit hook so bad code doesn't get committed. Then also run pylint, flake8 and bandit in the CI (GitHub Actions) on every pull request and fail the build if the pylint score drops below some number like 9 or bandit finds anything medium or high.

**4. What are the tangible improvements in code quality, readability and security?**

Pylint score went from 6.27 to 10/10, flake8 has 0 warnings now and bandit has 0 issues (it had 1 medium). The code is more readable because of docstrings, snake_case names and f-strings. For security, the backup file can't run code when loaded anymore since it's json instead of pickle. It's also more reliable: files are closed properly, the shared list bug is gone and bad orders/statuses now get rejected with a message instead of being silently accepted.
