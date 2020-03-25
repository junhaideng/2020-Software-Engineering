- 代码格式遵循python一般的代码规范，pycharm 支持`自动格式化`
- pycharm 中含有 TODO， 标记你需要做的工作(格式为`# TODO: `)

- `写注释`，`写注释`，`写注释`

- 模板中可以使用软链接就不要使用硬链接(按照[这里]( https://docs.djangoproject.com/en/3.0/topics/http/urls/#reverse-resolution-of-urls )写)

- git commit的时候，对不同类型的修改分开commit， 尽量不要使用`git add .`之类的一次性添加方式，请分别commit然后说明对应的修改

- push 代码的时候请详细的说明你修改的内容，并最好和team members 确认一下

- 代码中间存在任何的问题，或者有更好的修改建议，可以在github上发起 `issues`



<hr>

附git commit 描述:

格式  `type: <description>`

type:

- `feat`：新功能（feature）
- `fix`：修补bug
- `docs`：文档（documentation）
- `style`： 格式（不影响代码运行的变动）
- `refactor`：重构（即不是新增功能，也不是修改bug的代码变动）
- `test`：增加测试
- `chore`：构建过程或辅助工具的变动
- `add`: 添加某个文件等
- `change`: 对某个文件进行改变，但不改变原来的功能

