import rss from "@astrojs/rss";

export function GET() {
  // 导入所有 .md 文件，eager 表示立即加载而不是懒加载
  let allPosts = import.meta.glob("./posts/*.md", { eager: true });
  // 将对象转换为数组
  let posts = Object.values(allPosts);

  // 对文章进行排序，按文章编号降序排列
  posts = posts.sort((a, b) => {
    // 从 URL 中提取文章编号
    const getPostNumber = (url) =>
      parseInt(url.split("/posts/")[1].split("-")[0]);
    return getPostNumber(b.url) - getPostNumber(a.url);
  });

  // 只保留最新的12篇文章
  posts = posts.slice(0, 12);

  // 生成 RSS feed
  return rss({
    // RSS 标题
    title: "Af1周刊",
    // RSS 描述
    description: "记录 af1 的思考",
    // 网站地址
    site: "https://af1.fun/",
    // 自定义数据：添加图片和关注挑战相关信息
    customData: `<image><url>https://gw.alipayobjects.com/zos/k/qv/coffee-2-icon.png</url></image><follow_challenge><feedId>41147805276726275</feedId><userId>42909600318350336</userId></follow_challenge>`,
    // 处理每篇文章的信息
    items: posts.map((item) => {
      // 从 URL 中提取期号和标题
      const [issueNumber, issueTitle] = item.url.split("/posts/")[1].split("-");
      // 组合完整标题
      const title = `第${issueNumber}期 - ${issueTitle}`;
      return {
        link: item.url,           // 文章链接
        title,                    // 文章标题
        description: item.compiledContent(), // 文章内容
        pubDate: item.frontmatter.date,     // 发布日期
      };
    }),
  });
}
