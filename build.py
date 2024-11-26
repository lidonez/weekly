import os
import httpx
import re
import urllib.parse

def fetch_ci_time(file_path):
    url = f"https://api.github.com/repos/lidonez/weekly/commits?path={file_path}&page=1&per_page=1"
    response = httpx.get(url)
    ci_time = response.json()[0]["commit"]["committer"]["date"].split("T")[0]
    return ci_time

if __name__ == "__main__":
    with open('README.md', 'w') as readme_file, open('RECENT.md', 'w') as recent_file:
        readme_file.write("# af1周刊\n\n> 记录 af1 的不枯燥生活，一些些的思考 ，Fork 自用可见 [开发文档](https://github.com/tw93/weekly/blob/main/Deploy.md)，期待你玩得开心~\n\n")

        for root, dirs, filenames in os.walk('./src/pages/posts'):
            def get_number(filename):
                numbers = re.findall(r"(\d+)", filename)
                return float(numbers[0]) if numbers else 0  # 如果没有找到数字，返回0作为默认值
            
            filenames = sorted(filenames, key=get_number, reverse=True)

        for index, name in enumerate(filenames):
            if name.endswith('.md'):
                file_path = urllib.parse.quote(name)
                old_title = name.split('.md')[0]
                url = f'https://af1.fun/posts/{old_title}'
                title = f'第 {old_title.split("-")[0]} 期 - {old_title.split("-")[1]}'
                readme_md = f'* [{title}]({url})\n'
                num = int(old_title.split('-')[0])

                if index < 5:
                    modified = fetch_ci_time(f'/src/pages/posts/{file_path}')
                    recent_md = f'* [{title}]({url}) - {modified}\n'
                    recent_file.write(recent_md)

                readme_file.write(readme_md)
