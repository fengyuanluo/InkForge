# Changelog

## [0.11.0](https://github.com/fengyuanluo/InkForge/compare/v0.10.0...v0.11.0) (2026-08-18)


### ✨ 新功能

* **agent:** 支持世界书条目与回滚 ([#59](https://github.com/fengyuanluo/InkForge/issues/59)) ([b02549d](https://github.com/fengyuanluo/InkForge/commit/b02549d8ab8dc050478f98d8e95601c95ade3295))
* **agent:** 支持主 Agent 自定义标识（颜色与图标） ([#282](https://github.com/fengyuanluo/InkForge/issues/282)) ([b802c4d](https://github.com/fengyuanluo/InkForge/commit/b802c4d2543938a6fc61fc92c03754d3e9f8ae55))
* **agent:** 支持用户消息图片附件输入 ([#229](https://github.com/fengyuanluo/InkForge/issues/229)) ([2c12697](https://github.com/fengyuanluo/InkForge/commit/2c126978b101dc3c76b43556e7017084f27f97f2))
* **agent:** 支持规则全局与项目作用域 ([#269](https://github.com/fengyuanluo/InkForge/issues/269)) ([0fb578a](https://github.com/fengyuanluo/InkForge/commit/0fb578aa9c7ace66436f71331029dc82a76b316f))
* **agent:** 添加角色工具与回滚支持 ([#70](https://github.com/fengyuanluo/InkForge/issues/70)) ([4d2bbf0](https://github.com/fengyuanluo/InkForge/commit/4d2bbf06bef79b9fd97f2be414c6a5b779c5c865))
* **backend:** 为编辑工具引入模糊匹配与归一化机制 ([#165](https://github.com/fengyuanluo/InkForge/issues/165)) ([5805078](https://github.com/fengyuanluo/InkForge/commit/580507862debbe66d7ea221fc6deb339da71c211))
* **characters:** 添加角色管理功能 ([#64](https://github.com/fengyuanluo/InkForge/issues/64)) ([1d1626a](https://github.com/fengyuanluo/InkForge/commit/1d1626a316c5bcd0471f54807ae29a1ee81df918))
* **corpus:** add managed corpus RAG ([9b51049](https://github.com/fengyuanluo/InkForge/commit/9b51049e835e5d54b421675dff887027e5f1220e))
* **corpus:** add managed corpus RAG ([a1359bf](https://github.com/fengyuanluo/InkForge/commit/a1359bfbfdccad50bef4abc7e3f25af35802a11c))
* **desktop:** 支持应用内自动更新 ([#99](https://github.com/fengyuanluo/InkForge/issues/99)) ([bcd6eb9](https://github.com/fengyuanluo/InkForge/commit/bcd6eb94fe846c4237b89ffdad87d620ec7706b0))
* **desktop:** 支持数据备份、迁移、还原与自定义数据目录 ([#275](https://github.com/fengyuanluo/InkForge/issues/275)) ([23a1fac](https://github.com/fengyuanluo/InkForge/commit/23a1fac7e14d9184ebf2e583a8d451ef068cb80a))
* **desktop:** 添加壳层国际化支持 ([#223](https://github.com/fengyuanluo/InkForge/issues/223)) ([90f26c1](https://github.com/fengyuanluo/InkForge/commit/90f26c16a764c941124a3e70c8b2693b32a5f1d9))
* **desktop:** 添加桌面端应用 ([#29](https://github.com/fengyuanluo/InkForge/issues/29)) ([77c7789](https://github.com/fengyuanluo/InkForge/commit/77c7789e322b3a7ee029c4837272bf8a7c10df28))
* **fonts:** 引入 fontsource 字体支持 ([#294](https://github.com/fengyuanluo/InkForge/issues/294)) ([c135ee3](https://github.com/fengyuanluo/InkForge/commit/c135ee338975bf3330f179e3eba360ad12727a22))
* **frontend:** 添加 PWA 支持实现可安装应用 ([#56](https://github.com/fengyuanluo/InkForge/issues/56)) ([bd623fb](https://github.com/fengyuanluo/InkForge/commit/bd623fb73c87733a58e3d521cf9f066bcc0ccde7))
* **frontend:** 添加全局状态栏 ([#71](https://github.com/fengyuanluo/InkForge/issues/71)) ([d584d56](https://github.com/fengyuanluo/InkForge/commit/d584d560a6e05747655a4538593da48eaee87fbe))
* **frontend:** 补齐前端国际化文案并对齐英文翻译 ([#21](https://github.com/fengyuanluo/InkForge/issues/21)) ([59d4249](https://github.com/fengyuanluo/InkForge/commit/59d4249bfdfdb2b5867a789a7951e5812de8a011))
* **import:** 支持 TXT 分卷导入 ([#197](https://github.com/fengyuanluo/InkForge/issues/197)) ([4c781ce](https://github.com/fengyuanluo/InkForge/commit/4c781ce36a2baa4b5b1f8d2e82e51b72b659f28f))
* **settings:** 支持自定义基础字号与编辑器字号 ([#300](https://github.com/fengyuanluo/InkForge/issues/300)) ([ac6da38](https://github.com/fengyuanluo/InkForge/commit/ac6da382907886940fb17121d4a2b5bf6742cbcc))
* **telemetry:** 接入 PostHog 远程错误遥测 ([#305](https://github.com/fengyuanluo/InkForge/issues/305)) ([08d47ae](https://github.com/fengyuanluo/InkForge/commit/08d47aef1bd421993c3b2a952b69a2b468cbd8eb))
* **writing:** 支持章节导出 ([#195](https://github.com/fengyuanluo/InkForge/issues/195)) ([44171e8](https://github.com/fengyuanluo/InkForge/commit/44171e86010c858540b2a23e78e11d01e1ef5532))
* 完善项目 README 文档 ([ca919a2](https://github.com/fengyuanluo/InkForge/commit/ca919a2f376937da1cd7aa8179a735bf45c8896c))


### 🐛 问题修复

* **agent_runtime:** 修复 LLM 调用无超时保护且盲目重试导致会话卡死的问题 ([#261](https://github.com/fengyuanluo/InkForge/issues/261)) ([46535a0](https://github.com/fengyuanluo/InkForge/commit/46535a0dbd652aad50369657d8e297aad3f4b48f))
* **agent:** 优化会话运行状态提示 ([#122](https://github.com/fengyuanluo/InkForge/issues/122)) ([04c6e2e](https://github.com/fengyuanluo/InkForge/commit/04c6e2e6639c21594a90c9d5d9a5fe607c7a9dcc))
* **agent:** 优化用户消息展开动画 ([#120](https://github.com/fengyuanluo/InkForge/issues/120)) ([00d9cc8](https://github.com/fengyuanluo/InkForge/commit/00d9cc89a12984462f5a8eb80d0b3d372aa22446))
* **agent:** 修复 ask_user 问题面板内容无法滚动的问题 ([#249](https://github.com/fengyuanluo/InkForge/issues/249)) ([2921d0a](https://github.com/fengyuanluo/InkForge/commit/2921d0aa743aaf418d07277bed9f59af67508f57))
* **agent:** 修复 subagent 回滚状态恢复 ([#60](https://github.com/fengyuanluo/InkForge/issues/60)) ([b5fa608](https://github.com/fengyuanluo/InkForge/commit/b5fa60852a1031f9626e0fff201b719da77cb4c0))
* **agent:** 修复中断暂停状态的会话无法恢复的问题 ([#267](https://github.com/fengyuanluo/InkForge/issues/267)) ([6029bc3](https://github.com/fengyuanluo/InkForge/commit/6029bc37a53cff4054ed08f7dcca626b29398453))
* **agent:** 修复会话切换模型不生效 ([#91](https://github.com/fengyuanluo/InkForge/issues/91)) ([26ef7f3](https://github.com/fengyuanluo/InkForge/commit/26ef7f3beb202eb182b56ed483c144852be6d9c6))
* **agent:** 修复会话生命周期竞态导致取消和恢复异常的问题 ([#307](https://github.com/fengyuanluo/InkForge/issues/307)) ([c1430df](https://github.com/fengyuanluo/InkForge/commit/c1430df5a6a6181942f7327206bf51e3c5ba5bc2))
* **agent:** 修复会话结束后设置仍锁定的问题 ([#137](https://github.com/fengyuanluo/InkForge/issues/137)) ([103c392](https://github.com/fengyuanluo/InkForge/commit/103c392043f2eb246a974e431e40d0e15058a391))
* **agent:** 修复会话重连后流式事件丢失 ([#94](https://github.com/fengyuanluo/InkForge/issues/94)) ([018749c](https://github.com/fengyuanluo/InkForge/commit/018749caeea11f98d5f8405f17f7868949b3dbba))
* **agent:** 修复回滚时卷章节数不同步的问题 ([#117](https://github.com/fengyuanluo/InkForge/issues/117)) ([0e9bf90](https://github.com/fengyuanluo/InkForge/commit/0e9bf908fb4f323f8737bcd7866ac54c4130e669))
* **agent:** 修复子智能体派发配置 ([#111](https://github.com/fengyuanluo/InkForge/issues/111)) ([8906741](https://github.com/fengyuanluo/InkForge/commit/89067410aee4246a7a912e61bfba46f50aeef946))
* **agent:** 修复工具刷新失效问题 ([#185](https://github.com/fengyuanluo/InkForge/issues/185)) ([905aae2](https://github.com/fengyuanluo/InkForge/commit/905aae2574d2dd2dc15ffd771d0aa00f0cdc0c3e))
* **agent:** 修复工具调用未并行执行的问题 ([#266](https://github.com/fengyuanluo/InkForge/issues/266)) ([aefcd90](https://github.com/fengyuanluo/InkForge/commit/aefcd90f1004f2bf8af887ff785d8532eb982492))
* **agent:** 修复并行工具调用时唯一约束冲突的问题 ([#271](https://github.com/fengyuanluo/InkForge/issues/271)) ([5dbe377](https://github.com/fengyuanluo/InkForge/commit/5dbe3772a78ac56be85ae19ae23881185c20e4b4))
* **agent:** 修复异常消息导致的僵尸会话 ([#123](https://github.com/fengyuanluo/InkForge/issues/123)) ([84b95fe](https://github.com/fengyuanluo/InkForge/commit/84b95fec91a65679d4f7a729515c4012b011af06))
* **agent:** 修复旧会话配置无法恢复的问题 ([#202](https://github.com/fengyuanluo/InkForge/issues/202)) ([ac9a59b](https://github.com/fengyuanluo/InkForge/commit/ac9a59bea251a6bed4fb4ffcde005e74ee665151))
* **agent:** 修复流式消息底部跟随失效的问题 ([#119](https://github.com/fengyuanluo/InkForge/issues/119)) ([d79d3ed](https://github.com/fengyuanluo/InkForge/commit/d79d3edc1e6e967dd20752645bc52c0e95fe6bb8))
* **agent:** 修复编辑工具转义空白匹配失败的问题 ([#214](https://github.com/fengyuanluo/InkForge/issues/214)) ([649b87b](https://github.com/fengyuanluo/InkForge/commit/649b87b801458bfd3b1c44e84215a299b8eaa174))
* **agent:** 修复跨页面切换导致的侧边栏状态丢失问题 ([#178](https://github.com/fengyuanluo/InkForge/issues/178)) ([22b9a37](https://github.com/fengyuanluo/InkForge/commit/22b9a37c018ab64828cc7fdb97cbc1fa2b923d7e))
* **agent:** 修复重启后会话设置持续锁定的问题 ([#216](https://github.com/fengyuanluo/InkForge/issues/216)) ([33555ff](https://github.com/fengyuanluo/InkForge/commit/33555ff2c4d3a369938fd95e22fe64f276320a64))
* **agent:** 完善子智能体工具状态展示 ([#118](https://github.com/fengyuanluo/InkForge/issues/118)) ([a908536](https://github.com/fengyuanluo/InkForge/commit/a9085361cc32b46cc689c51a8d400c03ba0a1592))
* **agent:** 工具数量超限不再中断会话并返回错误结果 ([#293](https://github.com/fengyuanluo/InkForge/issues/293)) ([b35a744](https://github.com/fengyuanluo/InkForge/commit/b35a744e702e30a02b488f9948c433602ae3ff2a))
* **agent:** 清理不可达的会话检查点 ([#184](https://github.com/fengyuanluo/InkForge/issues/184)) ([8908120](https://github.com/fengyuanluo/InkForge/commit/890812052a3542dd5a1e799753206d67f108cf54))
* **agent:** 移除子计划依赖并改用笔记大纲 ([#15](https://github.com/fengyuanluo/InkForge/issues/15)) ([da97a8b](https://github.com/fengyuanluo/InkForge/commit/da97a8be36256a814677a20d540f853713f496f5))
* **agent:** 避免中断会话普通消息状态冲突 ([#177](https://github.com/fengyuanluo/InkForge/issues/177)) ([787669b](https://github.com/fengyuanluo/InkForge/commit/787669b51dc6a6a1e6b34184a6acf3e38504d854))
* **agent:** 防止会话检查点泄露模型密钥 ([#92](https://github.com/fengyuanluo/InkForge/issues/92)) ([0342427](https://github.com/fengyuanluo/InkForge/commit/034242754890db39d2296f3b489c2c2317eb37e7))
* **agent:** 限制智能体列表高度并支持滚动 ([#268](https://github.com/fengyuanluo/InkForge/issues/268)) ([fa44696](https://github.com/fengyuanluo/InkForge/commit/fa44696ea94d7b65c16e6d07f7a88642e3e8a7b2))
* **assistant:** 使用稳定的 diff section type ([#50](https://github.com/fengyuanluo/InkForge/issues/50)) ([27decdc](https://github.com/fengyuanluo/InkForge/commit/27decdcdf4bfe1fb6404d73a552fa1cc53958876))
* **backend:** 修复 LLM 长响应被超时中断的问题 ([#277](https://github.com/fengyuanluo/InkForge/issues/277)) ([3259325](https://github.com/fengyuanluo/InkForge/commit/32593253ba58143731dba5eb8f359b82234353c1))
* **backend:** 修复 Ollama Cloud 地址覆盖导致的模型调用失败问题 ([#146](https://github.com/fengyuanluo/InkForge/issues/146)) ([b5d116d](https://github.com/fengyuanluo/InkForge/commit/b5d116d065dfa9db24ee8635a8d97b6cb8e2e9cd))
* **backend:** 修复 Windows 后台任务队列阻塞的问题 ([#147](https://github.com/fengyuanluo/InkForge/issues/147)) ([cf1ffa1](https://github.com/fengyuanluo/InkForge/commit/cf1ffa1e0c7b47e1c38c7a7019bcb8e91f38791f))
* **backend:** 修复Windows上后台任务事件无法实时同步的问题 ([#148](https://github.com/fengyuanluo/InkForge/issues/148)) ([f4e83e1](https://github.com/fengyuanluo/InkForge/commit/f4e83e1c2e8affb07029750c64d2d6bd0f1779b3))
* **backend:** 修复会话标题生成异常 ([#108](https://github.com/fengyuanluo/InkForge/issues/108)) ([429ee53](https://github.com/fengyuanluo/InkForge/commit/429ee53f10f6f9cd3723b758259c833b4d708316))
* **backend:** 修复开发服务器运行时配置异常 ([#152](https://github.com/fengyuanluo/InkForge/issues/152)) ([e5e93ec](https://github.com/fengyuanluo/InkForge/commit/e5e93ec324ca28ae0e6e06e698c59e97367da7b8))
* **backend:** 修复测试夹具重复初始化导致后端测试耗时过长的问题 ([#241](https://github.com/fengyuanluo/InkForge/issues/241)) ([a355e7f](https://github.com/fengyuanluo/InkForge/commit/a355e7f16a5afc14da98cc238fc4a021a9e73973))
* **backend:** 修复离线环境下的分词表加载失败的问题 ([#187](https://github.com/fengyuanluo/InkForge/issues/187)) ([169d40b](https://github.com/fengyuanluo/InkForge/commit/169d40b7410ef238f18cb669936e17473b7696cd))
* **backend:** 修复部分提供商流式 token 用量缺失的问题 ([#158](https://github.com/fengyuanluo/InkForge/issues/158)) ([16376e9](https://github.com/fengyuanluo/InkForge/commit/16376e9baa618cc91ce74217f5a354e74ec01d9f))
* **backend:** 去重会话标题后台任务 ([#82](https://github.com/fengyuanluo/InkForge/issues/82)) ([afd9650](https://github.com/fengyuanluo/InkForge/commit/afd96506fff12d006383bedaae83c8273349a8c6))
* **backend:** 完善后端分发构建与启动入口 ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* **backend:** 完善后端构建与分发流程 ([#27](https://github.com/fengyuanluo/InkForge/issues/27)) ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* **backend:** 完善后端构建与分发流程 ([#27](https://github.com/fengyuanluo/InkForge/issues/27)) ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* **background:** 修复孤儿后台任务无法自动清理的问题 ([#83](https://github.com/fengyuanluo/InkForge/issues/83)) ([643531d](https://github.com/fengyuanluo/InkForge/commit/643531d73f86a860832305651bdc03a829ba136b))
* **build:** 修复 wheel 重复收录导致的构建失败 ([#125](https://github.com/fengyuanluo/InkForge/issues/125)) ([3c4e2d0](https://github.com/fengyuanluo/InkForge/commit/3c4e2d0c45896499fd0182617ccc24c45c9db2f3))
* **build:** 修正 electron-builder 配置并启用 changelog 作者显示 ([#13](https://github.com/fengyuanluo/InkForge/issues/13)) ([82532ee](https://github.com/fengyuanluo/InkForge/commit/82532ee37eb92e6965056b0e56c41c9a37fbbc8b))
* **ci:** 修复 Docker 推送 403 与版本号同步缺失 ([ed002f5](https://github.com/fengyuanluo/InkForge/commit/ed002f5e276402f5302675fa4ff6688c2acdc6a4))
* **ci:** 修复 release PR 合并命令参数解析 ([cf42194](https://github.com/fengyuanluo/InkForge/commit/cf421944b77747de1b4c78b8925621d85e74f461))
* **ci:** 修复 release-please 未更新后端版本号及镜像版本 ([#17](https://github.com/fengyuanluo/InkForge/issues/17)) ([de2bbdc](https://github.com/fengyuanluo/InkForge/commit/de2bbdc611cfb2615bc5be1987d4a82066dcd6e9))
* **ci:** 修复桌面发布流程 ([#33](https://github.com/fengyuanluo/InkForge/issues/33)) ([9f100fc](https://github.com/fengyuanluo/InkForge/commit/9f100fc8c4ab75f09f5fd5262cfbe7ca66e62353))
* **ci:** 修正 release-please manifest 配置结构 ([3bf931b](https://github.com/fengyuanluo/InkForge/commit/3bf931bdc53f244f01faf8115dca453e3232dd18))
* **ci:** 合并 release PR 前增加 checkout ([e1bf61a](https://github.com/fengyuanluo/InkForge/commit/e1bf61a01fc477a73076d77b433fd42113bf1c2f))
* **ci:** 同步 uv.lock 并修正后端包名 ([#19](https://github.com/fengyuanluo/InkForge/issues/19)) ([344bd82](https://github.com/fengyuanluo/InkForge/commit/344bd82c5ac43ad85203f8d09ad340e5e4d46e18))
* **ci:** 移除 PR 自查清单强制校验 ([#180](https://github.com/fengyuanluo/InkForge/issues/180)) ([54df8c1](https://github.com/fengyuanluo/InkForge/commit/54df8c1635f8ff1d7ba37f2289649ab0758af9bd))
* **ci:** 等待 release PR 可合并后再自动合并 ([#23](https://github.com/fengyuanluo/InkForge/issues/23)) ([d868fc6](https://github.com/fengyuanluo/InkForge/commit/d868fc6647d0f5cd8097f3e19c55a4f1c8546233))
* **ci:** 调整发布打包流程 ([#31](https://github.com/fengyuanluo/InkForge/issues/31)) ([f83451a](https://github.com/fengyuanluo/InkForge/commit/f83451a76225daa2c4d1669e93ef9f7f5309f52b))
* **ci:** 跳过发布 PR 检查 ([#174](https://github.com/fengyuanluo/InkForge/issues/174)) ([2286422](https://github.com/fengyuanluo/InkForge/commit/22864220d8f9732255587c3c921e0b21132a5d2d))
* **dashboard:** 修复调用记录时间未转换时区的问题 ([#204](https://github.com/fengyuanluo/InkForge/issues/204)) ([da977a8](https://github.com/fengyuanluo/InkForge/commit/da977a8311b8effbed9506f204bb97eb2d8af6d7))
* **db:** 修复 checkpoints.db 体积膨胀导致无法启动的问题 ([#303](https://github.com/fengyuanluo/InkForge/issues/303)) ([8c7cc10](https://github.com/fengyuanluo/InkForge/commit/8c7cc1000ee2566845439be409eb4157c49e48cd))
* **desktop:** uv 安装 TLS 证书错误时自动重试 ([#292](https://github.com/fengyuanluo/InkForge/issues/292)) ([79bad9b](https://github.com/fengyuanluo/InkForge/commit/79bad9b56e3a149aa0e66b3ba842ba8a9abe4736))
* **desktop:** 为桌面端运行环境添加国内下载源 ([#126](https://github.com/fengyuanluo/InkForge/issues/126)) ([5ba142e](https://github.com/fengyuanluo/InkForge/commit/5ba142e50d5fef9f6f425d56cc5612264fe09d14))
* **desktop:** 优化运行时连接流程 ([#199](https://github.com/fengyuanluo/InkForge/issues/199)) ([83c78ad](https://github.com/fengyuanluo/InkForge/commit/83c78ad119f3cc0c083fb15312af19673d3b4340))
* **desktop:** 修复 macOS 运行时与安装包校验异常 ([#215](https://github.com/fengyuanluo/InkForge/issues/215)) ([8ebac44](https://github.com/fengyuanluo/InkForge/commit/8ebac44ab083b00b2de394f740badcc45c8773a0))
* **desktop:** 修复 PyPI 镜像 wheel 文件 403 导致桌面更新失败的问题 ([#315](https://github.com/fengyuanluo/InkForge/issues/315)) ([fd99c8b](https://github.com/fengyuanluo/InkForge/commit/fd99c8b157be8251c3b3e4a21bfe4899b56c2fbe))
* **desktop:** 修复 Socket 首次连接失败导致启动中断的问题 ([#248](https://github.com/fengyuanluo/InkForge/issues/248)) ([7b84765](https://github.com/fengyuanluo/InkForge/commit/7b847652037b165f3f7129e59c3564ce617a290c))
* **desktop:** 修复 Windows 构建样式解析 ([#37](https://github.com/fengyuanluo/InkForge/issues/37)) ([e837bb1](https://github.com/fengyuanluo/InkForge/commit/e837bb14ea17d2a3ef46b0de6d6a72590f3778a9))
* **desktop:** 修复启动时窗口延迟显示的问题 ([#246](https://github.com/fengyuanluo/InkForge/issues/246)) ([6d0e05f](https://github.com/fengyuanluo/InkForge/commit/6d0e05f97753a3bcdd329be6f9a311b07714b4b6))
* **desktop:** 修复更新元数据缺失导致检查报错的问题 ([#239](https://github.com/fengyuanluo/InkForge/issues/239)) ([3b77aab](https://github.com/fengyuanluo/InkForge/commit/3b77aabe38134b34f46331d687fd0ca7ba4e8217))
* **desktop:** 修复更新日志渲染 ([#102](https://github.com/fengyuanluo/InkForge/issues/102)) ([2b75f25](https://github.com/fengyuanluo/InkForge/commit/2b75f25b1d08ecccbc4e9b7bee1e727b21fe24bf))
* **desktop:** 修复本地后端 Socket 代理连接失败的问题 ([#209](https://github.com/fengyuanluo/InkForge/issues/209)) ([7ffbd78](https://github.com/fengyuanluo/InkForge/commit/7ffbd78ea937e45a93d4faa571ef1434050f9f98))
* **desktop:** 修复本地后端启动 ([#43](https://github.com/fengyuanluo/InkForge/issues/43)) ([12440f7](https://github.com/fengyuanluo/InkForge/commit/12440f715495a2755c81a7be794426ca2cb7027b))
* **desktop:** 修复本地运行时安装 ([#41](https://github.com/fengyuanluo/InkForge/issues/41)) ([f77988b](https://github.com/fengyuanluo/InkForge/commit/f77988ba27449fb0708bfcce6395027f4e067ea3))
* **desktop:** 修复桌面端主题与字体无法跟随前端同步的问题 ([#157](https://github.com/fengyuanluo/InkForge/issues/157)) ([a2f8ebf](https://github.com/fengyuanluo/InkForge/commit/a2f8ebf495a67fa68d30c181fcdcdc6bd4afe70f))
* **desktop:** 修复系统缺失 tar 导致运行环境安装失败的问题 ([#188](https://github.com/fengyuanluo/InkForge/issues/188)) ([9685c19](https://github.com/fengyuanluo/InkForge/commit/9685c19d4058a3083a29d54dc00455110ab768de))
* **desktop:** 完善运行环境调试信息处理 ([#196](https://github.com/fengyuanluo/InkForge/issues/196)) ([39f3e55](https://github.com/fengyuanluo/InkForge/commit/39f3e55653e30d2cba7dece7425839a4ebae4d75))
* **desktop:** 限制 setup 错误内容高度 ([#314](https://github.com/fengyuanluo/InkForge/issues/314)) ([adaefb9](https://github.com/fengyuanluo/InkForge/commit/adaefb9b1b489597929654886807487a64cb7821))
* **editor:** 修复移动端正文点击重复呼出键盘的问题 ([#226](https://github.com/fengyuanluo/InkForge/issues/226)) ([79d03fa](https://github.com/fengyuanluo/InkForge/commit/79d03fa3c9f32dc8183e7b2ce234d747c12bef5d))
* **frontend:** 修复 Agent 侧边栏模型图标显示 ([#54](https://github.com/fengyuanluo/InkForge/issues/54)) ([9eeaaff](https://github.com/fengyuanluo/InkForge/commit/9eeaaff74c83a8d492eeb8fd3aa096017a89804c))
* **frontend:** 修复 Agent 消息完成重新挂载的问题 ([#61](https://github.com/fengyuanluo/InkForge/issues/61)) ([10e2e53](https://github.com/fengyuanluo/InkForge/commit/10e2e53811853d2b26c1bcdec5dd1152a02f1223))
* **frontend:** 修复 Agent 消息流式展示顺序 ([#63](https://github.com/fengyuanluo/InkForge/issues/63)) ([9b4ee74](https://github.com/fengyuanluo/InkForge/commit/9b4ee74f4e0f0481cba5f5c021ca0b61aa06c0f9))
* **frontend:** 修复 streamdown 流式渲染的最大更新深度崩溃问题 ([#272](https://github.com/fengyuanluo/InkForge/issues/272)) ([ab4b9f5](https://github.com/fengyuanluo/InkForge/commit/ab4b9f55c0e108998252747b0f54be6a5b62d2b4))
* **frontend:** 修复世界书开关状态错乱的问题 ([#138](https://github.com/fengyuanluo/InkForge/issues/138)) ([7d5eb27](https://github.com/fengyuanluo/InkForge/commit/7d5eb27da67edb5fdb3cc0aed4649a10892c08ae))
* **frontend:** 修复仪表盘图表日期范围与标签重叠的问题 ([#264](https://github.com/fengyuanluo/InkForge/issues/264)) ([e3996ba](https://github.com/fengyuanluo/InkForge/commit/e3996ba34703bb7e92b86b7e03f3feb6e98fe3c8))
* **frontend:** 修复卡初始化的问题并增强连接失败诊断信息 ([#287](https://github.com/fengyuanluo/InkForge/issues/287)) ([04acb43](https://github.com/fengyuanluo/InkForge/commit/04acb43764c2b1261a2de7b4ee2a27acfed4e03b))
* **frontend:** 修复发送新消息后上一条 Assistant 轮次 toolbar 消失的问题 ([#273](https://github.com/fengyuanluo/InkForge/issues/273)) ([ae8eda2](https://github.com/fengyuanluo/InkForge/commit/ae8eda2d162e6e65057f20ecc1582055548789f7))
* **frontend:** 修复同行内粘贴文本被拆分换行的问题 ([#258](https://github.com/fengyuanluo/InkForge/issues/258)) ([45c3d6a](https://github.com/fengyuanluo/InkForge/commit/45c3d6a19950dfd9f57c4d9bd3164f428453bba5))
* **frontend:** 修复已删除项目仍可打开的问题 ([#129](https://github.com/fengyuanluo/InkForge/issues/129)) ([0542e8f](https://github.com/fengyuanluo/InkForge/commit/0542e8faeab65ae34292ac6d329a61e7772a4e68))
* **frontend:** 修复提示词编辑内容丢失和本地修改提示缺失的问题 ([#140](https://github.com/fengyuanluo/InkForge/issues/140)) ([954d552](https://github.com/fengyuanluo/InkForge/commit/954d5529c5941ac3172cf5a3b6b1d1cb636431db))
* **frontend:** 修复桌面端后端资源地址解析异常 ([#136](https://github.com/fengyuanluo/InkForge/issues/136)) ([09c570f](https://github.com/fengyuanluo/InkForge/commit/09c570f4ac0b96b88427eed48de76da80ef9e525))
* **frontend:** 修复移动端编辑器菜单点击无效导致复制粘贴不可用的问题 ([#260](https://github.com/fengyuanluo/InkForge/issues/260)) ([ba4ba07](https://github.com/fengyuanluo/InkForge/commit/ba4ba07c0e00723e400ec476d714abc476492174))
* **frontend:** 修复编辑器剪贴板换行处理 ([#189](https://github.com/fengyuanluo/InkForge/issues/189)) ([95daf32](https://github.com/fengyuanluo/InkForge/commit/95daf32c59fc4931dd52dec07f7737e76661b676))
* **frontend:** 修复规则编辑区布局 ([#85](https://github.com/fengyuanluo/InkForge/issues/85)) ([025efad](https://github.com/fengyuanluo/InkForge/commit/025efad2f6ddf624b7d37242bfd180f8fa1ad4e2))
* **frontend:** 取消提供商任务类型筛选 ([#143](https://github.com/fengyuanluo/InkForge/issues/143)) ([f582c8e](https://github.com/fengyuanluo/InkForge/commit/f582c8ef1b4bd98e3e3ee4f461fb4e0341f7ed23))
* **frontend:** 完善移动端适配 ([#25](https://github.com/fengyuanluo/InkForge/issues/25)) ([a971904](https://github.com/fengyuanluo/InkForge/commit/a971904f00466b53203aa87fb146330aad5e710a))
* **frontend:** 对齐 Agent 工具消息注册 ([#55](https://github.com/fengyuanluo/InkForge/issues/55)) ([b7942f5](https://github.com/fengyuanluo/InkForge/commit/b7942f5cab56836dbeb3f837e4e6ad5deff373b3))
* **frontend:** 收起下拉框时不再误关闭设置面板 ([#297](https://github.com/fengyuanluo/InkForge/issues/297)) ([c4e0b47](https://github.com/fengyuanluo/InkForge/commit/c4e0b479a5642c7804dbdf68d448b913605284a1))
* **frontend:** 新建角色后自动切换标签 ([#191](https://github.com/fengyuanluo/InkForge/issues/191)) ([8f35b51](https://github.com/fengyuanluo/InkForge/commit/8f35b51b38670982764b7615d64106d9944329ee))
* **frontend:** 调整 Agent 工具消息展示 ([#62](https://github.com/fengyuanluo/InkForge/issues/62)) ([f6ccfbb](https://github.com/fengyuanluo/InkForge/commit/f6ccfbb2d853ac009a13def1b96d5cad1043cffa))
* **frontend:** 防止写作编辑内容丢失 ([#116](https://github.com/fengyuanluo/InkForge/issues/116)) ([06698db](https://github.com/fengyuanluo/InkForge/commit/06698dbb1a400b3cebadc7f237527dc53aa0e0e5))
* **index:** 修复分块配置保存使用旧输入值的问题 ([#250](https://github.com/fengyuanluo/InkForge/issues/250)) ([ed75ce4](https://github.com/fengyuanluo/InkForge/commit/ed75ce46a9be88a6044277d74abf5fe11123bf16))
* **index:** 修复索引取消清理与轮询导致的性能问题 ([#86](https://github.com/fengyuanluo/InkForge/issues/86)) ([73fa08e](https://github.com/fengyuanluo/InkForge/commit/73fa08e0f2c7e8049058e085837a45feb5cfeb28))
* **mobile:** 修复移动端布局适配问题 ([#96](https://github.com/fengyuanluo/InkForge/issues/96)) ([f396b34](https://github.com/fengyuanluo/InkForge/commit/f396b34066577be9a9a3e5bbef4ace3192b7b1f4))
* **projects:** 修复项目列表加载不完全导致分页、搜索和排序失效的问题 ([#284](https://github.com/fengyuanluo/InkForge/issues/284)) ([82af99e](https://github.com/fengyuanluo/InkForge/commit/82af99e687ff0d57842a70489d39146eb5191059))
* **providers:** 修复目录中部分提供商端点 URL 缺失的问题 ([#230](https://github.com/fengyuanluo/InkForge/issues/230)) ([0006c90](https://github.com/fengyuanluo/InkForge/commit/0006c906b8c878c07859d3e2b7afda02f4b2e2a1))
* **providers:** 避免图标请求阻塞连接操作 ([#183](https://github.com/fengyuanluo/InkForge/issues/183)) ([70d9419](https://github.com/fengyuanluo/InkForge/commit/70d9419832496b519ad629abf062fde3063d7b70))
* **release:** 统一跨平台产物命名 ([#100](https://github.com/fengyuanluo/InkForge/issues/100)) ([56def22](https://github.com/fengyuanluo/InkForge/commit/56def22bf42fa660b0b1459929c7f928f1e02c09))
* **settings:** 锁定运行期间的智能体配置 ([#93](https://github.com/fengyuanluo/InkForge/issues/93)) ([6afd4b0](https://github.com/fengyuanluo/InkForge/commit/6afd4b0e9fa8c106917e8d3ec07f32255c30f7e4))
* **storage:** 修复章节排序更新冲突 ([#141](https://github.com/fengyuanluo/InkForge/issues/141)) ([dade8e8](https://github.com/fengyuanluo/InkForge/commit/dade8e899dbddf6ae8ab8eae190aa1a3e81be034))
* **storage:** 清理数据库关联运行时数据 ([#238](https://github.com/fengyuanluo/InkForge/issues/238)) ([b8d2ca5](https://github.com/fengyuanluo/InkForge/commit/b8d2ca5d58d64ecaf2acee919a0638104b0dce72))
* **summary:** 修复跨卷删除章节导致区间摘要丢失的问题 ([#225](https://github.com/fengyuanluo/InkForge/issues/225)) ([9ecaa07](https://github.com/fengyuanluo/InkForge/commit/9ecaa07fb38e9eb845135aabe0336d21adc0966c))
* **test:** 移除引用已迁移路径与偶发卡死的失效测试 ([eb638df](https://github.com/fengyuanluo/InkForge/commit/eb638df74a1754c65351ec924098edabd7c15ebe))


### ⚡ 性能优化

* **backend:** 优化检索索引状态与模型提供商列表接口性能 ([#291](https://github.com/fengyuanluo/InkForge/issues/291)) ([c77b264](https://github.com/fengyuanluo/InkForge/commit/c77b264eafc2c15e78793bd01d5cc32f6d7e4437))
* **desktop:** 缩减桌面安装包体积 ([#313](https://github.com/fengyuanluo/InkForge/issues/313)) ([0ecbc54](https://github.com/fengyuanluo/InkForge/commit/0ecbc5440c7bf24585886f4743dfb037109460ee))
* **frontend:** 虚拟化 Agent 消息列表并合并流式增量渲染 ([#257](https://github.com/fengyuanluo/InkForge/issues/257)) ([87aa448](https://github.com/fengyuanluo/InkForge/commit/87aa448add26bce1dfb9dc925a6db72473d63ebd))
* **world-info:** 虚拟化世界书条目列表并优化拖拽排序 ([#254](https://github.com/fengyuanluo/InkForge/issues/254)) ([ad94f34](https://github.com/fengyuanluo/InkForge/commit/ad94f340c043999d5f8d6dc25580c559cec7edb0))


### ♻️ 代码重构

* **agent:** 重构 Agent 工具上下文与中断恢复链路 ([#110](https://github.com/fengyuanluo/InkForge/issues/110)) ([5ab5a2b](https://github.com/fengyuanluo/InkForge/commit/5ab5a2bc722267ff0e7af7e13e5b1f1c4bc2de78))
* **agent:** 重构 mention XML 流转链路 ([#78](https://github.com/fengyuanluo/InkForge/issues/78)) ([28e7b16](https://github.com/fengyuanluo/InkForge/commit/28e7b16aeb6c9d8288cd2d27210f075883a5d0ac))
* **agent:** 重构 Skill 功能 ([#77](https://github.com/fengyuanluo/InkForge/issues/77)) ([97e1f5e](https://github.com/fengyuanluo/InkForge/commit/97e1f5e20083de7b2f1ca22073bbbd42314abe9c))
* **backend:** 统一后台运行日志输出 ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* **dashboard:** 调用记录详情存储优化并记录工具引用 ([#107](https://github.com/fengyuanluo/InkForge/issues/107)) ([c25b2c1](https://github.com/fengyuanluo/InkForge/commit/c25b2c16673e860e8e0df3d614cec5169f3a2ff7))
* **frontend:** 将仪表盘图表库替换为 Nivo ([#72](https://github.com/fengyuanluo/InkForge/issues/72)) ([3cbd4b7](https://github.com/fengyuanluo/InkForge/commit/3cbd4b7389e39bf80d26d7ac8a24a85ae1a39a05))
* **index:** 重构索引面板与进度展示 ([#80](https://github.com/fengyuanluo/InkForge/issues/80)) ([eff0886](https://github.com/fengyuanluo/InkForge/commit/eff0886281ac277ccc49e03ab6cba8c3ec0c2eb3))
* **model:** 统一高级参数配置 ([#109](https://github.com/fengyuanluo/InkForge/issues/109)) ([f672970](https://github.com/fengyuanluo/InkForge/commit/f672970f13567721b2ce6d731419e0ee1214a2e4))
* **prompt-chains:** 重构提示词管理页面 ([#95](https://github.com/fengyuanluo/InkForge/issues/95)) ([73db522](https://github.com/fengyuanluo/InkForge/commit/73db52232f506edb9bda8e76156382aef4508310))
* **summary:** 重构摘要生成面板与交互体验 ([#84](https://github.com/fengyuanluo/InkForge/issues/84)) ([8e16a19](https://github.com/fengyuanluo/InkForge/commit/8e16a19204ff9718fcf7a25b38719a80c9c2cf52))


### 📚 文档

* **readme:** 同步项目文档内容 ([#124](https://github.com/fengyuanluo/InkForge/issues/124)) ([736779c](https://github.com/fengyuanluo/InkForge/commit/736779cebea82f1c69e699d887a6a76c9cda2ef8))
* **readme:** 更新项目介绍与发布提示 ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* 更新 README 章节结构 ([#155](https://github.com/fengyuanluo/InkForge/issues/155)) ([154fab7](https://github.com/fengyuanluo/InkForge/commit/154fab748fd17b448cba173821234b7bc0acf70c))
* 更新README ([#79](https://github.com/fengyuanluo/InkForge/issues/79)) ([869b98c](https://github.com/fengyuanluo/InkForge/commit/869b98c248dd442c96165a47883b2ff011d697df))
* 添加二开开发规范 ([94f3d61](https://github.com/fengyuanluo/InkForge/commit/94f3d618e429b0d10863b77fd8b8d0846dfb9253))


### ✅ 测试

* **desktop:** 新增基于源码后端的本地开发模式 ([#304](https://github.com/fengyuanluo/InkForge/issues/304)) ([84d63f1](https://github.com/fengyuanluo/InkForge/commit/84d63f1aa6905896596818427f3f3275bcebc40e))
* **frontend:** 新增 Agent 会话生命周期 E2E 测试 ([#308](https://github.com/fengyuanluo/InkForge/issues/308)) ([9478baf](https://github.com/fengyuanluo/InkForge/commit/9478baf2f46317bd859deb21042c0bb02ce55441))


### 🔧 杂项

* **agent:** 允许Agent会话记住输入历史和未发送草稿 ([#316](https://github.com/fengyuanluo/InkForge/issues/316)) ([7c0b8f2](https://github.com/fengyuanluo/InkForge/commit/7c0b8f27dbb52f895492a24ca1c799e8cd7a9823))
* **agent:** 本地化适配工具权限展示文案 ([#112](https://github.com/fengyuanluo/InkForge/issues/112)) ([362c129](https://github.com/fengyuanluo/InkForge/commit/362c12903beee21373e9db124f6fafb5b08dfb41))
* **agent:** 添加会话计时器 ([#262](https://github.com/fengyuanluo/InkForge/issues/262)) ([70e9652](https://github.com/fengyuanluo/InkForge/commit/70e96528066389d7cb30329be6bbcd2d455f34e3))
* **agent:** 补充角色页 Agent 侧边栏 ([#176](https://github.com/fengyuanluo/InkForge/issues/176)) ([ad4988e](https://github.com/fengyuanluo/InkForge/commit/ad4988e85adedcc96911fca85338eff48daad488))
* **agent:** 调整内置智能体定义 ([#115](https://github.com/fengyuanluo/InkForge/issues/115)) ([3dcdbb8](https://github.com/fengyuanluo/InkForge/commit/3dcdbb82255e79a10059b69f8c3a41d966a8ed5e))
* **agent:** 调整内置智能体提示词 ([#121](https://github.com/fengyuanluo/InkForge/issues/121)) ([211c7b0](https://github.com/fengyuanluo/InkForge/commit/211c7b04f687bac675c6700ebe503fb598b4e73a))
* **agent:** 限制子智能体委派与提问能力 ([#90](https://github.com/fengyuanluo/InkForge/issues/90)) ([9999283](https://github.com/fengyuanluo/InkForge/commit/999928376012548bfca968aab270f38e7bcd3a83))
* **api:** 世界书改为项目强绑定 ([#73](https://github.com/fengyuanluo/InkForge/issues/73)) ([393add6](https://github.com/fengyuanluo/InkForge/commit/393add677c755ddd60bf1019ebd6110b75b462b3))
* **backend:** 为 OpenAI Compatible 提供商添加思考强度支持 ([#192](https://github.com/fengyuanluo/InkForge/issues/192)) ([195615f](https://github.com/fengyuanluo/InkForge/commit/195615f4e22f0c33442e96d072a726de7363599d))
* **backend:** 添加 justfile 后端命令封装 ([#69](https://github.com/fengyuanluo/InkForge/issues/69)) ([d66b128](https://github.com/fengyuanluo/InkForge/commit/d66b1282ef7a4934a11827e793b894937f0cfc86))
* **backend:** 调整摘要上下文结构 ([#106](https://github.com/fengyuanluo/InkForge/issues/106)) ([6b2cf6d](https://github.com/fengyuanluo/InkForge/commit/6b2cf6d8376e61daee7902a796dcda73342ade28))
* **backend:** 迁移类型检查到 ty ([#68](https://github.com/fengyuanluo/InkForge/issues/68)) ([d404696](https://github.com/fengyuanluo/InkForge/commit/d40469688379706a176958cf6407d747a8c6b85c))
* **build:** 迁移前端与桌面端构建至 Vite+ ([#97](https://github.com/fengyuanluo/InkForge/issues/97)) ([c77fd90](https://github.com/fengyuanluo/InkForge/commit/c77fd907ce9a0a55eac24e3fc49094c03c188a25))
* **desktop:** 添加桌面端菜单栏 ([#221](https://github.com/fengyuanluo/InkForge/issues/221)) ([0d9bbe8](https://github.com/fengyuanluo/InkForge/commit/0d9bbe8dc9f5cfb186cf2a196b40b4d577c113b1))
* **desktop:** 添加窗口状态记忆能力 ([#159](https://github.com/fengyuanluo/InkForge/issues/159)) ([eb0e1a4](https://github.com/fengyuanluo/InkForge/commit/eb0e1a4816bcd6d9b0682a8c96190eb52e3fc3a6))
* **editor:** 优化编辑器体验 ([#219](https://github.com/fengyuanluo/InkForge/issues/219)) ([f3554d4](https://github.com/fengyuanluo/InkForge/commit/f3554d47ea549dffebda9ad4f2289dc904cdfa6f))
* **editor:** 新增单条正文内容长度限制 ([#193](https://github.com/fengyuanluo/InkForge/issues/193)) ([cb87f42](https://github.com/fengyuanluo/InkForge/commit/cb87f42a8803584e664519696ddce6aca6883def))
* **editor:** 新增段落自动缩进设置 ([#311](https://github.com/fengyuanluo/InkForge/issues/311)) ([4024a67](https://github.com/fengyuanluo/InkForge/commit/4024a67de7afc02048420ab374143c75997928ea))
* **editor:** 新增自动转换半角符号设置 ([#312](https://github.com/fengyuanluo/InkForge/issues/312)) ([30fb71e](https://github.com/fengyuanluo/InkForge/commit/30fb71e2ee050cc384c1635193db489f35582568))
* **frontend:** 添加 Oxfmt 格式化支持 ([#67](https://github.com/fengyuanluo/InkForge/issues/67)) ([40e2efd](https://github.com/fengyuanluo/InkForge/commit/40e2efd7890749378e76958d85a9da0819789fdf))
* **frontend:** 添加最近打开项目入口 ([#104](https://github.com/fengyuanluo/InkForge/issues/104)) ([16d6f4b](https://github.com/fengyuanluo/InkForge/commit/16d6f4bb5b45edee3e1876c95e0783aea15a2f91))
* **frontend:** 添加系统默认字体选项 ([#128](https://github.com/fengyuanluo/InkForge/issues/128)) ([3980ee2](https://github.com/fengyuanluo/InkForge/commit/3980ee2af3d85c66016b0d2ada45c7058596ef8c))
* **frontend:** 统一设置面板加载行为 ([#52](https://github.com/fengyuanluo/InkForge/issues/52)) ([798e8ad](https://github.com/fengyuanluo/InkForge/commit/798e8add8df5d24c93bbf0d1118049f6b4412ea4))
* **frontend:** 补齐前端界面 i18n 文案接入 ([#51](https://github.com/fengyuanluo/InkForge/issues/51)) ([7932bf7](https://github.com/fengyuanluo/InkForge/commit/7932bf7e4f3175746677f1be990164ca64e3bc24))
* **frontend:** 调整设置面板模型禁用态 ([#53](https://github.com/fengyuanluo/InkForge/issues/53)) ([86449ec](https://github.com/fengyuanluo/InkForge/commit/86449ece001aa8dbf210d322d19522ed81d8f620))
* **frontend:** 调整设置面板自动保存 ([#46](https://github.com/fengyuanluo/InkForge/issues/46)) ([a94d0eb](https://github.com/fengyuanluo/InkForge/commit/a94d0ebf7683e2b864c5ba3539ede0f38bce66e9))
* **frontend:** 迁移前端检查到 Oxlint ([#66](https://github.com/fengyuanluo/InkForge/issues/66)) ([7c10648](https://github.com/fengyuanluo/InkForge/commit/7c10648bcd31ab6f71248e8af5aa4d0f7414ac51))
* **frontend:** 适配角色与世界书移动端顶栏 ([#74](https://github.com/fengyuanluo/InkForge/issues/74)) ([1824117](https://github.com/fengyuanluo/InkForge/commit/1824117893de708fe7c802379021885236e2ea2b))
* **main:** release 0.10.0 ([#270](https://github.com/fengyuanluo/InkForge/issues/270)) ([3bc330f](https://github.com/fengyuanluo/InkForge/commit/3bc330f4a786dc6ebb02421cdf62fb2d876cedee))
* **main:** release 0.2.0 ([#6](https://github.com/fengyuanluo/InkForge/issues/6)) ([005ef9e](https://github.com/fengyuanluo/InkForge/commit/005ef9eed1f8a4b2a23964a2aeed7855d4dfc3f1))
* **main:** release 0.2.1 ([#10](https://github.com/fengyuanluo/InkForge/issues/10)) ([1e530a0](https://github.com/fengyuanluo/InkForge/commit/1e530a0c08d9b117965d1991d4883b997b3eb0d4))
* **main:** release 0.2.2 ([#12](https://github.com/fengyuanluo/InkForge/issues/12)) ([00df636](https://github.com/fengyuanluo/InkForge/commit/00df63652a7b964e81ebcf0bed775f14bf21aece))
* **main:** release 0.2.3 ([#14](https://github.com/fengyuanluo/InkForge/issues/14)) ([af06d65](https://github.com/fengyuanluo/InkForge/commit/af06d65e5c3d6da6e8a272fea9a715b284ba370e))
* **main:** release 0.2.4 ([#16](https://github.com/fengyuanluo/InkForge/issues/16)) ([1b6dec7](https://github.com/fengyuanluo/InkForge/commit/1b6dec7987c099ae942474984479d546b4cbe3b5))
* **main:** release 0.2.5 ([#18](https://github.com/fengyuanluo/InkForge/issues/18)) ([1183b9f](https://github.com/fengyuanluo/InkForge/commit/1183b9feca00b4fc1e83562a5a8fba4b1db22da1))
* **main:** release 0.2.6 ([#20](https://github.com/fengyuanluo/InkForge/issues/20)) ([0fe9586](https://github.com/fengyuanluo/InkForge/commit/0fe9586f363614a1e3ae401b0c6218ed9556beea))
* **main:** release 0.3.0 ([#22](https://github.com/fengyuanluo/InkForge/issues/22)) ([388bc0a](https://github.com/fengyuanluo/InkForge/commit/388bc0a4185d342a891b0d2ffaa59dff2e3ad356))
* **main:** release 0.3.1 ([#24](https://github.com/fengyuanluo/InkForge/issues/24)) ([3b82f84](https://github.com/fengyuanluo/InkForge/commit/3b82f84b5370c1bcb6692a6ffa0e2698e65435b9))
* **main:** release 0.3.2 ([#26](https://github.com/fengyuanluo/InkForge/issues/26)) ([4eef46b](https://github.com/fengyuanluo/InkForge/commit/4eef46b952291e61751a648b6355716a22792da4))
* **main:** release 0.3.3 ([#28](https://github.com/fengyuanluo/InkForge/issues/28)) ([7e70e38](https://github.com/fengyuanluo/InkForge/commit/7e70e383e17691b415f2030affa8f0ae8095191f))
* **main:** release 0.4.0 ([#30](https://github.com/fengyuanluo/InkForge/issues/30)) ([65c22af](https://github.com/fengyuanluo/InkForge/commit/65c22af61369cf3485f46787164a19bcd9d697a6))
* **main:** release 0.4.1 ([#32](https://github.com/fengyuanluo/InkForge/issues/32)) ([f0e588c](https://github.com/fengyuanluo/InkForge/commit/f0e588ca456b8bd3bfc6dad82ce8656b67a1bf0e))
* **main:** release 0.4.2 ([#34](https://github.com/fengyuanluo/InkForge/issues/34)) ([e2a0441](https://github.com/fengyuanluo/InkForge/commit/e2a044154f20e14e6a6db5e4a359028ce5a01faf))
* **main:** release 0.4.3 ([#36](https://github.com/fengyuanluo/InkForge/issues/36)) ([b9faa2a](https://github.com/fengyuanluo/InkForge/commit/b9faa2abe5cf61a54081d7496a6ece723e0388fc))
* **main:** release 0.4.4 ([#38](https://github.com/fengyuanluo/InkForge/issues/38)) ([9b53e9c](https://github.com/fengyuanluo/InkForge/commit/9b53e9c214ad5888b48f8377de1f5f7c08539fd5))
* **main:** release 0.4.5 ([#40](https://github.com/fengyuanluo/InkForge/issues/40)) ([04e43f2](https://github.com/fengyuanluo/InkForge/commit/04e43f29c78bff2e1cecbd2a2f6c6f16e112ce3c))
* **main:** release 0.4.6 ([#42](https://github.com/fengyuanluo/InkForge/issues/42)) ([c6ed162](https://github.com/fengyuanluo/InkForge/commit/c6ed16219542bf6ecbb78cf10b5cb7e63a4dd298))
* **main:** release 0.4.7 ([#44](https://github.com/fengyuanluo/InkForge/issues/44)) ([2767509](https://github.com/fengyuanluo/InkForge/commit/2767509ab19f42946000e7c31ae5a4a3d8f6cb68))
* **main:** release 0.4.8 ([#47](https://github.com/fengyuanluo/InkForge/issues/47)) ([0609000](https://github.com/fengyuanluo/InkForge/commit/06090009bb6b7bf4f0c97161823bbc01fbb709f9))
* **main:** release 0.4.9 ([#49](https://github.com/fengyuanluo/InkForge/issues/49)) ([175d6ab](https://github.com/fengyuanluo/InkForge/commit/175d6aba716ddf4c14b9e0c40147539fa29e5c2a))
* **main:** release 0.5.0 ([#57](https://github.com/fengyuanluo/InkForge/issues/57)) ([a2bf0ef](https://github.com/fengyuanluo/InkForge/commit/a2bf0efebdaeff20e02bdb054d630fd6512a5715))
* **main:** release 0.6.0 ([#65](https://github.com/fengyuanluo/InkForge/issues/65)) ([d04fc7a](https://github.com/fengyuanluo/InkForge/commit/d04fc7a8a0e3eeaae160f1ed2298387d2d36e5ce))
* **main:** release 0.6.1 ([#75](https://github.com/fengyuanluo/InkForge/issues/75)) ([5c9a268](https://github.com/fengyuanluo/InkForge/commit/5c9a2684a5f568bcf80001186df3e653ed6f3a49))
* **main:** release 0.6.2 ([#88](https://github.com/fengyuanluo/InkForge/issues/88)) ([4bbddc9](https://github.com/fengyuanluo/InkForge/commit/4bbddc98b953a4f8d71ef0354e17113afbe1bbfa))
* **main:** release 0.7.0 ([#98](https://github.com/fengyuanluo/InkForge/issues/98)) ([87cf421](https://github.com/fengyuanluo/InkForge/commit/87cf4215c1e3430361e40805186bc9121a4f9f31))
* **main:** release 0.7.1 ([#101](https://github.com/fengyuanluo/InkForge/issues/101)) ([18223f2](https://github.com/fengyuanluo/InkForge/commit/18223f2033c2f71fffab62027aef5641df0e1d96))
* **main:** release 0.7.2 ([#103](https://github.com/fengyuanluo/InkForge/issues/103)) ([8b406e3](https://github.com/fengyuanluo/InkForge/commit/8b406e37fe5586df35b3e02edfcd10228520339b))
* **main:** release 0.7.3 ([#105](https://github.com/fengyuanluo/InkForge/issues/105)) ([7ea4437](https://github.com/fengyuanluo/InkForge/commit/7ea443747f8e63cc4bb70c0a9b1c29dd6fa2904d))
* **main:** release 0.7.4 ([#114](https://github.com/fengyuanluo/InkForge/issues/114)) ([6f48df3](https://github.com/fengyuanluo/InkForge/commit/6f48df3667a92af5095e76b7702e06265a819ddd))
* **main:** release 0.7.5 ([#127](https://github.com/fengyuanluo/InkForge/issues/127)) ([2ef5b6d](https://github.com/fengyuanluo/InkForge/commit/2ef5b6dd153924abac3e983681ac2354219c7048))
* **main:** release 0.7.6 ([#149](https://github.com/fengyuanluo/InkForge/issues/149)) ([2c34499](https://github.com/fengyuanluo/InkForge/commit/2c34499fd130a6531cb3fd686944b908ba77bbf8))
* **main:** release 0.8.0 ([#173](https://github.com/fengyuanluo/InkForge/issues/173)) ([35f7648](https://github.com/fengyuanluo/InkForge/commit/35f764880cac30993fd7efd21cb8790398982d7f))
* **main:** release 0.8.1 ([#203](https://github.com/fengyuanluo/InkForge/issues/203)) ([c457d05](https://github.com/fengyuanluo/InkForge/commit/c457d05ce7971d2fab03d723d3fed8afb886c65a))
* **main:** release 0.9.0 ([#222](https://github.com/fengyuanluo/InkForge/issues/222)) ([8f52518](https://github.com/fengyuanluo/InkForge/commit/8f52518887a08dad2cb9c9fb29ab1b46d849aca6))
* **main:** release 0.9.1 ([#240](https://github.com/fengyuanluo/InkForge/issues/240)) ([60d7ec9](https://github.com/fengyuanluo/InkForge/commit/60d7ec9d88d1102ad5e14ad7182785625ae2287d))
* **main:** release 0.9.2 ([#256](https://github.com/fengyuanluo/InkForge/issues/256)) ([f0b726f](https://github.com/fengyuanluo/InkForge/commit/f0b726fc437c35c6d914a4f4a753f438e011ff21))
* **models:** 优化模型选择器并移除Provider图标上传 ([#87](https://github.com/fengyuanluo/InkForge/issues/87)) ([436f761](https://github.com/fengyuanluo/InkForge/commit/436f761611ee57c67bcf0cdad72284b85a9fafaf))
* **providers:** 优化内置提供商选取、刷新与调用 ([#89](https://github.com/fengyuanluo/InkForge/issues/89)) ([0fe4188](https://github.com/fengyuanluo/InkForge/commit/0fe418852730254789473fdcd96993136f7dabc2))
* **provider:** 新增 Anthropic Compatible 提供商 ([#208](https://github.com/fengyuanluo/InkForge/issues/208)) ([2000f79](https://github.com/fengyuanluo/InkForge/commit/2000f79d522bd4140994bc3ce1c59799f85baa30))
* **skills:** 优化技能配置体验 ([#218](https://github.com/fengyuanluo/InkForge/issues/218)) ([d7976c5](https://github.com/fengyuanluo/InkForge/commit/d7976c583bdd3bf6d3a67c9efc3231b941d4c167))
* **skill:** 添加内置写作技能 ([#113](https://github.com/fengyuanluo/InkForge/issues/113)) ([664d126](https://github.com/fengyuanluo/InkForge/commit/664d12632b63b8c363bc3ead66a1197a8ff56826))
* **status-bar:** 添加索引进度展示 ([#81](https://github.com/fengyuanluo/InkForge/issues/81)) ([84f94c7](https://github.com/fengyuanluo/InkForge/commit/84f94c725854e42d1e3a80cff82c707ebe30b643))
* **sync:** merge upstream main through 7c0b8f2 ([8b47096](https://github.com/fengyuanluo/InkForge/commit/8b4709667ab338806203a5106bb240e3c71d0945))
* **vscode:** 添加 VS Code 开发任务配置 ([#309](https://github.com/fengyuanluo/InkForge/issues/309)) ([94503b9](https://github.com/fengyuanluo/InkForge/commit/94503b921f42ab8a61b98365889929d4979477b6))
* 优化角色和世界书列表体验 ([#212](https://github.com/fengyuanluo/InkForge/issues/212)) ([191ed05](https://github.com/fengyuanluo/InkForge/commit/191ed05888ced345ca4a0b78f58dfacc8b832ab4))
* 添加压缩系统提示词选项 ([#263](https://github.com/fengyuanluo/InkForge/issues/263)) ([5dbc83d](https://github.com/fengyuanluo/InkForge/commit/5dbc83d2ef45ef341cd71b295664194a1934642d))
* 添加结构化 Issue 模板 ([#156](https://github.com/fengyuanluo/InkForge/issues/156)) ([9e3b8ad](https://github.com/fengyuanluo/InkForge/commit/9e3b8ad04912331507efa742d9963b7f1ed72883))
* 调整 Agent 会话命名与任务列表交互 ([#58](https://github.com/fengyuanluo/InkForge/issues/58)) ([741d2e3](https://github.com/fengyuanluo/InkForge/commit/741d2e369a37c11d28f3831fd5eb5d777b09ab46))


### 👷 CI/CD

* **desktop:** 修复多架构构建导致发布包损坏的问题 ([#247](https://github.com/fengyuanluo/InkForge/issues/247)) ([7ffe8cd](https://github.com/fengyuanluo/InkForge/commit/7ffe8cd1a254e2c2b892bb806d6c83e75edd156f))
* **package:** 优化发布缓存复用 ([#39](https://github.com/fengyuanluo/InkForge/issues/39)) ([68f9542](https://github.com/fengyuanluo/InkForge/commit/68f954246c1e1f9307313cda7c8e8f6082be2f8b))
* **release:** 修复每次 PR 都触发发版 ([#48](https://github.com/fengyuanluo/InkForge/issues/48)) ([5668036](https://github.com/fengyuanluo/InkForge/commit/5668036edb098c386ec8369867f21e21c9b0bd60))
* **release:** 等待 release PR 可合并 ([#35](https://github.com/fengyuanluo/InkForge/issues/35)) ([6105251](https://github.com/fengyuanluo/InkForge/commit/6105251aa84f173ca9eb998dd229e05e5f243ac2))
* 添加 PR 检查工作流 ([#172](https://github.com/fengyuanluo/InkForge/issues/172)) ([17ce3f7](https://github.com/fengyuanluo/InkForge/commit/17ce3f752348dd0c965ae9b6c360b48cedd7e22d))

## [0.10.0](https://github.com/fengyuanluo/InkForge/compare/v0.9.2...v0.10.0) (2026-08-16)


### ✨ 新功能

* **agent:** 支持主 Agent 自定义标识（颜色与图标） ([#282](https://github.com/fengyuanluo/InkForge/issues/282)) ([b802c4d](https://github.com/fengyuanluo/InkForge/commit/b802c4d2543938a6fc61fc92c03754d3e9f8ae55))
* **agent:** 支持规则全局与项目作用域 ([#269](https://github.com/fengyuanluo/InkForge/issues/269)) ([0fb578a](https://github.com/fengyuanluo/InkForge/commit/0fb578aa9c7ace66436f71331029dc82a76b316f))
* **desktop:** 支持数据备份、迁移、还原与自定义数据目录 ([#275](https://github.com/fengyuanluo/InkForge/issues/275)) ([23a1fac](https://github.com/fengyuanluo/InkForge/commit/23a1fac7e14d9184ebf2e583a8d451ef068cb80a))
* **fonts:** 引入 fontsource 字体支持 ([#294](https://github.com/fengyuanluo/InkForge/issues/294)) ([c135ee3](https://github.com/fengyuanluo/InkForge/commit/c135ee338975bf3330f179e3eba360ad12727a22))
* **settings:** 支持自定义基础字号与编辑器字号 ([#300](https://github.com/fengyuanluo/InkForge/issues/300)) ([ac6da38](https://github.com/fengyuanluo/InkForge/commit/ac6da382907886940fb17121d4a2b5bf6742cbcc))
* **telemetry:** 接入 PostHog 远程错误遥测 ([#305](https://github.com/fengyuanluo/InkForge/issues/305)) ([08d47ae](https://github.com/fengyuanluo/InkForge/commit/08d47aef1bd421993c3b2a952b69a2b468cbd8eb))


### 🐛 问题修复

* **agent:** 修复会话生命周期竞态导致取消和恢复异常的问题 ([#307](https://github.com/fengyuanluo/InkForge/issues/307)) ([c1430df](https://github.com/fengyuanluo/InkForge/commit/c1430df5a6a6181942f7327206bf51e3c5ba5bc2))
* **agent:** 修复并行工具调用时唯一约束冲突的问题 ([#271](https://github.com/fengyuanluo/InkForge/issues/271)) ([5dbe377](https://github.com/fengyuanluo/InkForge/commit/5dbe3772a78ac56be85ae19ae23881185c20e4b4))
* **agent:** 工具数量超限不再中断会话并返回错误结果 ([#293](https://github.com/fengyuanluo/InkForge/issues/293)) ([b35a744](https://github.com/fengyuanluo/InkForge/commit/b35a744e702e30a02b488f9948c433602ae3ff2a))
* **backend:** 修复 LLM 长响应被超时中断的问题 ([#277](https://github.com/fengyuanluo/InkForge/issues/277)) ([3259325](https://github.com/fengyuanluo/InkForge/commit/32593253ba58143731dba5eb8f359b82234353c1))
* **db:** 修复 checkpoints.db 体积膨胀导致无法启动的问题 ([#303](https://github.com/fengyuanluo/InkForge/issues/303)) ([8c7cc10](https://github.com/fengyuanluo/InkForge/commit/8c7cc1000ee2566845439be409eb4157c49e48cd))
* **desktop:** uv 安装 TLS 证书错误时自动重试 ([#292](https://github.com/fengyuanluo/InkForge/issues/292)) ([79bad9b](https://github.com/fengyuanluo/InkForge/commit/79bad9b56e3a149aa0e66b3ba842ba8a9abe4736))
* **frontend:** 修复 streamdown 流式渲染的最大更新深度崩溃问题 ([#272](https://github.com/fengyuanluo/InkForge/issues/272)) ([ab4b9f5](https://github.com/fengyuanluo/InkForge/commit/ab4b9f55c0e108998252747b0f54be6a5b62d2b4))
* **frontend:** 修复卡初始化的问题并增强连接失败诊断信息 ([#287](https://github.com/fengyuanluo/InkForge/issues/287)) ([04acb43](https://github.com/fengyuanluo/InkForge/commit/04acb43764c2b1261a2de7b4ee2a27acfed4e03b))
* **frontend:** 修复发送新消息后上一条 Assistant 轮次 toolbar 消失的问题 ([#273](https://github.com/fengyuanluo/InkForge/issues/273)) ([ae8eda2](https://github.com/fengyuanluo/InkForge/commit/ae8eda2d162e6e65057f20ecc1582055548789f7))
* **frontend:** 收起下拉框时不再误关闭设置面板 ([#297](https://github.com/fengyuanluo/InkForge/issues/297)) ([c4e0b47](https://github.com/fengyuanluo/InkForge/commit/c4e0b479a5642c7804dbdf68d448b913605284a1))
* **projects:** 修复项目列表加载不完全导致分页、搜索和排序失效的问题 ([#284](https://github.com/fengyuanluo/InkForge/issues/284)) ([82af99e](https://github.com/fengyuanluo/InkForge/commit/82af99e687ff0d57842a70489d39146eb5191059))


### ⚡ 性能优化

* **backend:** 优化检索索引状态与模型提供商列表接口性能 ([#291](https://github.com/fengyuanluo/InkForge/issues/291)) ([c77b264](https://github.com/fengyuanluo/InkForge/commit/c77b264eafc2c15e78793bd01d5cc32f6d7e4437))


### ✅ 测试

* **desktop:** 新增基于源码后端的本地开发模式 ([#304](https://github.com/fengyuanluo/InkForge/issues/304)) ([84d63f1](https://github.com/fengyuanluo/InkForge/commit/84d63f1aa6905896596818427f3f3275bcebc40e))
* **frontend:** 新增 Agent 会话生命周期 E2E 测试 ([#308](https://github.com/fengyuanluo/InkForge/issues/308)) ([9478baf](https://github.com/fengyuanluo/InkForge/commit/9478baf2f46317bd859deb21042c0bb02ce55441))

## [0.9.2](https://github.com/fengyuanluo/InkForge/compare/v0.9.1...v0.9.2) (2026-08-08)


### 🐛 问题修复

* **agent_runtime:** 修复 LLM 调用无超时保护且盲目重试导致会话卡死的问题 ([#261](https://github.com/fengyuanluo/InkForge/issues/261)) ([46535a0](https://github.com/fengyuanluo/InkForge/commit/46535a0dbd652aad50369657d8e297aad3f4b48f))
* **agent:** 修复中断暂停状态的会话无法恢复的问题 ([#267](https://github.com/fengyuanluo/InkForge/issues/267)) ([6029bc3](https://github.com/fengyuanluo/InkForge/commit/6029bc37a53cff4054ed08f7dcca626b29398453))
* **agent:** 修复工具调用未并行执行的问题 ([#266](https://github.com/fengyuanluo/InkForge/issues/266)) ([aefcd90](https://github.com/fengyuanluo/InkForge/commit/aefcd90f1004f2bf8af887ff785d8532eb982492))
* **agent:** 限制智能体列表高度并支持滚动 ([#268](https://github.com/fengyuanluo/InkForge/issues/268)) ([fa44696](https://github.com/fengyuanluo/InkForge/commit/fa44696ea94d7b65c16e6d07f7a88642e3e8a7b2))
* **frontend:** 修复仪表盘图表日期范围与标签重叠的问题 ([#264](https://github.com/fengyuanluo/InkForge/issues/264)) ([e3996ba](https://github.com/fengyuanluo/InkForge/commit/e3996ba34703bb7e92b86b7e03f3feb6e98fe3c8))
* **frontend:** 修复同行内粘贴文本被拆分换行的问题 ([#258](https://github.com/fengyuanluo/InkForge/issues/258)) ([45c3d6a](https://github.com/fengyuanluo/InkForge/commit/45c3d6a19950dfd9f57c4d9bd3164f428453bba5))
* **frontend:** 修复移动端编辑器菜单点击无效导致复制粘贴不可用的问题 ([#260](https://github.com/fengyuanluo/InkForge/issues/260)) ([ba4ba07](https://github.com/fengyuanluo/InkForge/commit/ba4ba07c0e00723e400ec476d714abc476492174))


### ⚡ 性能优化

* **frontend:** 虚拟化 Agent 消息列表并合并流式增量渲染 ([#257](https://github.com/fengyuanluo/InkForge/issues/257)) ([87aa448](https://github.com/fengyuanluo/InkForge/commit/87aa448add26bce1dfb9dc925a6db72473d63ebd))
* **world-info:** 虚拟化世界书条目列表并优化拖拽排序 ([#254](https://github.com/fengyuanluo/InkForge/issues/254)) ([ad94f34](https://github.com/fengyuanluo/InkForge/commit/ad94f340c043999d5f8d6dc25580c559cec7edb0))


### 🔧 杂项

* **agent:** 添加会话计时器 ([#262](https://github.com/fengyuanluo/InkForge/issues/262)) ([70e9652](https://github.com/fengyuanluo/InkForge/commit/70e96528066389d7cb30329be6bbcd2d455f34e3))
* 添加压缩系统提示词选项 ([#263](https://github.com/fengyuanluo/InkForge/issues/263)) ([5dbc83d](https://github.com/fengyuanluo/InkForge/commit/5dbc83d2ef45ef341cd71b295664194a1934642d))

## [0.9.1](https://github.com/fengyuanluo/InkForge/compare/v0.9.0...v0.9.1) (2026-08-05)


### 🐛 问题修复

* **agent:** 修复 ask_user 问题面板内容无法滚动的问题 ([#249](https://github.com/fengyuanluo/InkForge/issues/249)) ([2921d0a](https://github.com/fengyuanluo/InkForge/commit/2921d0aa743aaf418d07277bed9f59af67508f57))
* **backend:** 修复测试夹具重复初始化导致后端测试耗时过长的问题 ([#241](https://github.com/fengyuanluo/InkForge/issues/241)) ([a355e7f](https://github.com/fengyuanluo/InkForge/commit/a355e7f16a5afc14da98cc238fc4a021a9e73973))
* **desktop:** 修复 Socket 首次连接失败导致启动中断的问题 ([#248](https://github.com/fengyuanluo/InkForge/issues/248)) ([7b84765](https://github.com/fengyuanluo/InkForge/commit/7b847652037b165f3f7129e59c3564ce617a290c))
* **desktop:** 修复启动时窗口延迟显示的问题 ([#246](https://github.com/fengyuanluo/InkForge/issues/246)) ([6d0e05f](https://github.com/fengyuanluo/InkForge/commit/6d0e05f97753a3bcdd329be6f9a311b07714b4b6))
* **desktop:** 修复更新元数据缺失导致检查报错的问题 ([#239](https://github.com/fengyuanluo/InkForge/issues/239)) ([3b77aab](https://github.com/fengyuanluo/InkForge/commit/3b77aabe38134b34f46331d687fd0ca7ba4e8217))
* **index:** 修复分块配置保存使用旧输入值的问题 ([#250](https://github.com/fengyuanluo/InkForge/issues/250)) ([ed75ce4](https://github.com/fengyuanluo/InkForge/commit/ed75ce46a9be88a6044277d74abf5fe11123bf16))


### 👷 CI/CD

* **desktop:** 修复多架构构建导致发布包损坏的问题 ([#247](https://github.com/fengyuanluo/InkForge/issues/247)) ([7ffe8cd](https://github.com/fengyuanluo/InkForge/commit/7ffe8cd1a254e2c2b892bb806d6c83e75edd156f))

## [0.9.0](https://github.com/fengyuanluo/InkForge/compare/v0.8.1...v0.9.0) (2026-08-04)


### ✨ 新功能

* **agent:** 支持用户消息图片附件输入 ([#229](https://github.com/fengyuanluo/InkForge/issues/229)) ([2c12697](https://github.com/fengyuanluo/InkForge/commit/2c126978b101dc3c76b43556e7017084f27f97f2))
* **desktop:** 添加壳层国际化支持 ([#223](https://github.com/fengyuanluo/InkForge/issues/223)) ([90f26c1](https://github.com/fengyuanluo/InkForge/commit/90f26c16a764c941124a3e70c8b2693b32a5f1d9))


### 🐛 问题修复

* **editor:** 修复移动端正文点击重复呼出键盘的问题 ([#226](https://github.com/fengyuanluo/InkForge/issues/226)) ([79d03fa](https://github.com/fengyuanluo/InkForge/commit/79d03fa3c9f32dc8183e7b2ce234d747c12bef5d))
* **providers:** 修复目录中部分提供商端点 URL 缺失的问题 ([#230](https://github.com/fengyuanluo/InkForge/issues/230)) ([0006c90](https://github.com/fengyuanluo/InkForge/commit/0006c906b8c878c07859d3e2b7afda02f4b2e2a1))
* **storage:** 清理数据库关联运行时数据 ([#238](https://github.com/fengyuanluo/InkForge/issues/238)) ([b8d2ca5](https://github.com/fengyuanluo/InkForge/commit/b8d2ca5d58d64ecaf2acee919a0638104b0dce72))
* **summary:** 修复跨卷删除章节导致区间摘要丢失的问题 ([#225](https://github.com/fengyuanluo/InkForge/issues/225)) ([9ecaa07](https://github.com/fengyuanluo/InkForge/commit/9ecaa07fb38e9eb845135aabe0336d21adc0966c))


### 🔧 杂项

* **desktop:** 添加桌面端菜单栏 ([#221](https://github.com/fengyuanluo/InkForge/issues/221)) ([0d9bbe8](https://github.com/fengyuanluo/InkForge/commit/0d9bbe8dc9f5cfb186cf2a196b40b4d577c113b1))

## [0.8.1](https://github.com/fengyuanluo/InkForge/compare/v0.8.0...v0.8.1) (2026-07-31)


### 🐛 问题修复

* **agent:** 修复旧会话配置无法恢复的问题 ([#202](https://github.com/fengyuanluo/InkForge/issues/202)) ([ac9a59b](https://github.com/fengyuanluo/InkForge/commit/ac9a59bea251a6bed4fb4ffcde005e74ee665151))
* **agent:** 修复编辑工具转义空白匹配失败的问题 ([#214](https://github.com/fengyuanluo/InkForge/issues/214)) ([649b87b](https://github.com/fengyuanluo/InkForge/commit/649b87b801458bfd3b1c44e84215a299b8eaa174))
* **agent:** 修复重启后会话设置持续锁定的问题 ([#216](https://github.com/fengyuanluo/InkForge/issues/216)) ([33555ff](https://github.com/fengyuanluo/InkForge/commit/33555ff2c4d3a369938fd95e22fe64f276320a64))
* **dashboard:** 修复调用记录时间未转换时区的问题 ([#204](https://github.com/fengyuanluo/InkForge/issues/204)) ([da977a8](https://github.com/fengyuanluo/InkForge/commit/da977a8311b8effbed9506f204bb97eb2d8af6d7))
* **desktop:** 修复 macOS 运行时与安装包校验异常 ([#215](https://github.com/fengyuanluo/InkForge/issues/215)) ([8ebac44](https://github.com/fengyuanluo/InkForge/commit/8ebac44ab083b00b2de394f740badcc45c8773a0))
* **desktop:** 修复本地后端 Socket 代理连接失败的问题 ([#209](https://github.com/fengyuanluo/InkForge/issues/209)) ([7ffbd78](https://github.com/fengyuanluo/InkForge/commit/7ffbd78ea937e45a93d4faa571ef1434050f9f98))
* **frontend:** 新建角色后自动切换标签 ([#191](https://github.com/fengyuanluo/InkForge/issues/191)) ([8f35b51](https://github.com/fengyuanluo/InkForge/commit/8f35b51b38670982764b7615d64106d9944329ee))


### 🔧 杂项

* **editor:** 优化编辑器体验 ([#219](https://github.com/fengyuanluo/InkForge/issues/219)) ([f3554d4](https://github.com/fengyuanluo/InkForge/commit/f3554d47ea549dffebda9ad4f2289dc904cdfa6f))
* **provider:** 新增 Anthropic Compatible 提供商 ([#208](https://github.com/fengyuanluo/InkForge/issues/208)) ([2000f79](https://github.com/fengyuanluo/InkForge/commit/2000f79d522bd4140994bc3ce1c59799f85baa30))
* **skills:** 优化技能配置体验 ([#218](https://github.com/fengyuanluo/InkForge/issues/218)) ([d7976c5](https://github.com/fengyuanluo/InkForge/commit/d7976c583bdd3bf6d3a67c9efc3231b941d4c167))
* 优化角色和世界书列表体验 ([#212](https://github.com/fengyuanluo/InkForge/issues/212)) ([191ed05](https://github.com/fengyuanluo/InkForge/commit/191ed05888ced345ca4a0b78f58dfacc8b832ab4))

## [0.8.0](https://github.com/fengyuanluo/InkForge/compare/v0.7.6...v0.8.0) (2026-07-29)


### ✨ 新功能

* **backend:** 为编辑工具引入模糊匹配与归一化机制 ([#165](https://github.com/fengyuanluo/InkForge/issues/165)) ([5805078](https://github.com/fengyuanluo/InkForge/commit/580507862debbe66d7ea221fc6deb339da71c211))
* **import:** 支持 TXT 分卷导入 ([#197](https://github.com/fengyuanluo/InkForge/issues/197)) ([4c781ce](https://github.com/fengyuanluo/InkForge/commit/4c781ce36a2baa4b5b1f8d2e82e51b72b659f28f))
* **writing:** 支持章节导出 ([#195](https://github.com/fengyuanluo/InkForge/issues/195)) ([44171e8](https://github.com/fengyuanluo/InkForge/commit/44171e86010c858540b2a23e78e11d01e1ef5532))


### 🐛 问题修复

* **agent:** 修复工具刷新失效问题 ([#185](https://github.com/fengyuanluo/InkForge/issues/185)) ([905aae2](https://github.com/fengyuanluo/InkForge/commit/905aae2574d2dd2dc15ffd771d0aa00f0cdc0c3e))
* **agent:** 修复跨页面切换导致的侧边栏状态丢失问题 ([#178](https://github.com/fengyuanluo/InkForge/issues/178)) ([22b9a37](https://github.com/fengyuanluo/InkForge/commit/22b9a37c018ab64828cc7fdb97cbc1fa2b923d7e))
* **agent:** 清理不可达的会话检查点 ([#184](https://github.com/fengyuanluo/InkForge/issues/184)) ([8908120](https://github.com/fengyuanluo/InkForge/commit/890812052a3542dd5a1e799753206d67f108cf54))
* **agent:** 避免中断会话普通消息状态冲突 ([#177](https://github.com/fengyuanluo/InkForge/issues/177)) ([787669b](https://github.com/fengyuanluo/InkForge/commit/787669b51dc6a6a1e6b34184a6acf3e38504d854))
* **backend:** 修复离线环境下的分词表加载失败的问题 ([#187](https://github.com/fengyuanluo/InkForge/issues/187)) ([169d40b](https://github.com/fengyuanluo/InkForge/commit/169d40b7410ef238f18cb669936e17473b7696cd))
* **ci:** 移除 PR 自查清单强制校验 ([#180](https://github.com/fengyuanluo/InkForge/issues/180)) ([54df8c1](https://github.com/fengyuanluo/InkForge/commit/54df8c1635f8ff1d7ba37f2289649ab0758af9bd))
* **ci:** 跳过发布 PR 检查 ([#174](https://github.com/fengyuanluo/InkForge/issues/174)) ([2286422](https://github.com/fengyuanluo/InkForge/commit/22864220d8f9732255587c3c921e0b21132a5d2d))
* **desktop:** 优化运行时连接流程 ([#199](https://github.com/fengyuanluo/InkForge/issues/199)) ([83c78ad](https://github.com/fengyuanluo/InkForge/commit/83c78ad119f3cc0c083fb15312af19673d3b4340))
* **desktop:** 修复系统缺失 tar 导致运行环境安装失败的问题 ([#188](https://github.com/fengyuanluo/InkForge/issues/188)) ([9685c19](https://github.com/fengyuanluo/InkForge/commit/9685c19d4058a3083a29d54dc00455110ab768de))
* **desktop:** 完善运行环境调试信息处理 ([#196](https://github.com/fengyuanluo/InkForge/issues/196)) ([39f3e55](https://github.com/fengyuanluo/InkForge/commit/39f3e55653e30d2cba7dece7425839a4ebae4d75))
* **frontend:** 修复编辑器剪贴板换行处理 ([#189](https://github.com/fengyuanluo/InkForge/issues/189)) ([95daf32](https://github.com/fengyuanluo/InkForge/commit/95daf32c59fc4931dd52dec07f7737e76661b676))
* **providers:** 避免图标请求阻塞连接操作 ([#183](https://github.com/fengyuanluo/InkForge/issues/183)) ([70d9419](https://github.com/fengyuanluo/InkForge/commit/70d9419832496b519ad629abf062fde3063d7b70))


### 🔧 杂项

* **agent:** 补充角色页 Agent 侧边栏 ([#176](https://github.com/fengyuanluo/InkForge/issues/176)) ([ad4988e](https://github.com/fengyuanluo/InkForge/commit/ad4988e85adedcc96911fca85338eff48daad488))
* **backend:** 为 OpenAI Compatible 提供商添加思考强度支持 ([#192](https://github.com/fengyuanluo/InkForge/issues/192)) ([195615f](https://github.com/fengyuanluo/InkForge/commit/195615f4e22f0c33442e96d072a726de7363599d))
* **editor:** 新增单条正文内容长度限制 ([#193](https://github.com/fengyuanluo/InkForge/issues/193)) ([cb87f42](https://github.com/fengyuanluo/InkForge/commit/cb87f42a8803584e664519696ddce6aca6883def))


### 👷 CI/CD

* 添加 PR 检查工作流 ([#172](https://github.com/fengyuanluo/InkForge/issues/172)) ([17ce3f7](https://github.com/fengyuanluo/InkForge/commit/17ce3f752348dd0c965ae9b6c360b48cedd7e22d))

## [0.7.6](https://github.com/fengyuanluo/InkForge/compare/v0.7.5...v0.7.6) (2026-07-26)


### 🐛 问题修复

* **backend:** 修复Windows上后台任务事件无法实时同步的问题 ([#148](https://github.com/fengyuanluo/InkForge/issues/148)) ([f4e83e1](https://github.com/fengyuanluo/InkForge/commit/f4e83e1c2e8affb07029750c64d2d6bd0f1779b3))
* **backend:** 修复开发服务器运行时配置异常 ([#152](https://github.com/fengyuanluo/InkForge/issues/152)) ([e5e93ec](https://github.com/fengyuanluo/InkForge/commit/e5e93ec324ca28ae0e6e06e698c59e97367da7b8))
* **backend:** 修复部分提供商流式 token 用量缺失的问题 ([#158](https://github.com/fengyuanluo/InkForge/issues/158)) ([16376e9](https://github.com/fengyuanluo/InkForge/commit/16376e9baa618cc91ce74217f5a354e74ec01d9f))
* **desktop:** 修复桌面端主题与字体无法跟随前端同步的问题 ([#157](https://github.com/fengyuanluo/InkForge/issues/157)) ([a2f8ebf](https://github.com/fengyuanluo/InkForge/commit/a2f8ebf495a67fa68d30c181fcdcdc6bd4afe70f))


### 📚 文档

* 更新 README 章节结构 ([#155](https://github.com/fengyuanluo/InkForge/issues/155)) ([154fab7](https://github.com/fengyuanluo/InkForge/commit/154fab748fd17b448cba173821234b7bc0acf70c))


### 🔧 杂项

* **desktop:** 添加窗口状态记忆能力 ([#159](https://github.com/fengyuanluo/InkForge/issues/159)) ([eb0e1a4](https://github.com/fengyuanluo/InkForge/commit/eb0e1a4816bcd6d9b0682a8c96190eb52e3fc3a6))
* 添加结构化 Issue 模板 ([#156](https://github.com/fengyuanluo/InkForge/issues/156)) ([9e3b8ad](https://github.com/fengyuanluo/InkForge/commit/9e3b8ad04912331507efa742d9963b7f1ed72883))

## [0.7.5](https://github.com/fengyuanluo/InkForge/compare/v0.7.4...v0.7.5) (2026-07-26)


### 🐛 问题修复

* **agent:** 修复会话结束后设置仍锁定的问题 ([#137](https://github.com/fengyuanluo/InkForge/issues/137)) ([103c392](https://github.com/fengyuanluo/InkForge/commit/103c392043f2eb246a974e431e40d0e15058a391))
* **backend:** 修复 Ollama Cloud 地址覆盖导致的模型调用失败问题 ([#146](https://github.com/fengyuanluo/InkForge/issues/146)) ([b5d116d](https://github.com/fengyuanluo/InkForge/commit/b5d116d065dfa9db24ee8635a8d97b6cb8e2e9cd))
* **backend:** 修复 Windows 后台任务队列阻塞的问题 ([#147](https://github.com/fengyuanluo/InkForge/issues/147)) ([cf1ffa1](https://github.com/fengyuanluo/InkForge/commit/cf1ffa1e0c7b47e1c38c7a7019bcb8e91f38791f))
* **desktop:** 为桌面端运行环境添加国内下载源 ([#126](https://github.com/fengyuanluo/InkForge/issues/126)) ([5ba142e](https://github.com/fengyuanluo/InkForge/commit/5ba142e50d5fef9f6f425d56cc5612264fe09d14))
* **frontend:** 修复世界书开关状态错乱的问题 ([#138](https://github.com/fengyuanluo/InkForge/issues/138)) ([7d5eb27](https://github.com/fengyuanluo/InkForge/commit/7d5eb27da67edb5fdb3cc0aed4649a10892c08ae))
* **frontend:** 修复已删除项目仍可打开的问题 ([#129](https://github.com/fengyuanluo/InkForge/issues/129)) ([0542e8f](https://github.com/fengyuanluo/InkForge/commit/0542e8faeab65ae34292ac6d329a61e7772a4e68))
* **frontend:** 修复提示词编辑内容丢失和本地修改提示缺失的问题 ([#140](https://github.com/fengyuanluo/InkForge/issues/140)) ([954d552](https://github.com/fengyuanluo/InkForge/commit/954d5529c5941ac3172cf5a3b6b1d1cb636431db))
* **frontend:** 修复桌面端后端资源地址解析异常 ([#136](https://github.com/fengyuanluo/InkForge/issues/136)) ([09c570f](https://github.com/fengyuanluo/InkForge/commit/09c570f4ac0b96b88427eed48de76da80ef9e525))
* **frontend:** 取消提供商任务类型筛选 ([#143](https://github.com/fengyuanluo/InkForge/issues/143)) ([f582c8e](https://github.com/fengyuanluo/InkForge/commit/f582c8ef1b4bd98e3e3ee4f461fb4e0341f7ed23))
* **storage:** 修复章节排序更新冲突 ([#141](https://github.com/fengyuanluo/InkForge/issues/141)) ([dade8e8](https://github.com/fengyuanluo/InkForge/commit/dade8e899dbddf6ae8ab8eae190aa1a3e81be034))


### 🔧 杂项

* **frontend:** 添加系统默认字体选项 ([#128](https://github.com/fengyuanluo/InkForge/issues/128)) ([3980ee2](https://github.com/fengyuanluo/InkForge/commit/3980ee2af3d85c66016b0d2ada45c7058596ef8c))

## [0.7.4](https://github.com/fengyuanluo/InkForge/compare/v0.7.3...v0.7.4) (2026-07-25)


### 🐛 问题修复

* **agent:** 优化会话运行状态提示 ([#122](https://github.com/fengyuanluo/InkForge/issues/122)) ([04c6e2e](https://github.com/fengyuanluo/InkForge/commit/04c6e2e6639c21594a90c9d5d9a5fe607c7a9dcc))
* **agent:** 优化用户消息展开动画 ([#120](https://github.com/fengyuanluo/InkForge/issues/120)) ([00d9cc8](https://github.com/fengyuanluo/InkForge/commit/00d9cc89a12984462f5a8eb80d0b3d372aa22446))
* **agent:** 修复回滚时卷章节数不同步的问题 ([#117](https://github.com/fengyuanluo/InkForge/issues/117)) ([0e9bf90](https://github.com/fengyuanluo/InkForge/commit/0e9bf908fb4f323f8737bcd7866ac54c4130e669))
* **agent:** 修复异常消息导致的僵尸会话 ([#123](https://github.com/fengyuanluo/InkForge/issues/123)) ([84b95fe](https://github.com/fengyuanluo/InkForge/commit/84b95fec91a65679d4f7a729515c4012b011af06))
* **agent:** 修复流式消息底部跟随失效的问题 ([#119](https://github.com/fengyuanluo/InkForge/issues/119)) ([d79d3ed](https://github.com/fengyuanluo/InkForge/commit/d79d3edc1e6e967dd20752645bc52c0e95fe6bb8))
* **agent:** 完善子智能体工具状态展示 ([#118](https://github.com/fengyuanluo/InkForge/issues/118)) ([a908536](https://github.com/fengyuanluo/InkForge/commit/a9085361cc32b46cc689c51a8d400c03ba0a1592))
* **frontend:** 防止写作编辑内容丢失 ([#116](https://github.com/fengyuanluo/InkForge/issues/116)) ([06698db](https://github.com/fengyuanluo/InkForge/commit/06698dbb1a400b3cebadc7f237527dc53aa0e0e5))


### 📚 文档

* **readme:** 同步项目文档内容 ([#124](https://github.com/fengyuanluo/InkForge/issues/124)) ([736779c](https://github.com/fengyuanluo/InkForge/commit/736779cebea82f1c69e699d887a6a76c9cda2ef8))


### 🔧 杂项

* **agent:** 调整内置智能体定义 ([#115](https://github.com/fengyuanluo/InkForge/issues/115)) ([3dcdbb8](https://github.com/fengyuanluo/InkForge/commit/3dcdbb82255e79a10059b69f8c3a41d966a8ed5e))
* **agent:** 调整内置智能体提示词 ([#121](https://github.com/fengyuanluo/InkForge/issues/121)) ([211c7b0](https://github.com/fengyuanluo/InkForge/commit/211c7b04f687bac675c6700ebe503fb598b4e73a))
* **skill:** 添加内置写作技能 ([#113](https://github.com/fengyuanluo/InkForge/issues/113)) ([664d126](https://github.com/fengyuanluo/InkForge/commit/664d12632b63b8c363bc3ead66a1197a8ff56826))

## [0.7.3](https://github.com/fengyuanluo/InkForge/compare/v0.7.2...v0.7.3) (2026-07-19)


### 🐛 问题修复

* **agent:** 修复子智能体派发配置 ([#111](https://github.com/fengyuanluo/InkForge/issues/111)) ([8906741](https://github.com/fengyuanluo/InkForge/commit/89067410aee4246a7a912e61bfba46f50aeef946))
* **backend:** 修复会话标题生成异常 ([#108](https://github.com/fengyuanluo/InkForge/issues/108)) ([429ee53](https://github.com/fengyuanluo/InkForge/commit/429ee53f10f6f9cd3723b758259c833b4d708316))


### ♻️ 代码重构

* **agent:** 重构 Agent 工具上下文与中断恢复链路 ([#110](https://github.com/fengyuanluo/InkForge/issues/110)) ([5ab5a2b](https://github.com/fengyuanluo/InkForge/commit/5ab5a2bc722267ff0e7af7e13e5b1f1c4bc2de78))
* **dashboard:** 调用记录详情存储优化并记录工具引用 ([#107](https://github.com/fengyuanluo/InkForge/issues/107)) ([c25b2c1](https://github.com/fengyuanluo/InkForge/commit/c25b2c16673e860e8e0df3d614cec5169f3a2ff7))
* **model:** 统一高级参数配置 ([#109](https://github.com/fengyuanluo/InkForge/issues/109)) ([f672970](https://github.com/fengyuanluo/InkForge/commit/f672970f13567721b2ce6d731419e0ee1214a2e4))


### 🔧 杂项

* **agent:** 本地化适配工具权限展示文案 ([#112](https://github.com/fengyuanluo/InkForge/issues/112)) ([362c129](https://github.com/fengyuanluo/InkForge/commit/362c12903beee21373e9db124f6fafb5b08dfb41))
* **backend:** 调整摘要上下文结构 ([#106](https://github.com/fengyuanluo/InkForge/issues/106)) ([6b2cf6d](https://github.com/fengyuanluo/InkForge/commit/6b2cf6d8376e61daee7902a796dcda73342ade28))
* **frontend:** 添加最近打开项目入口 ([#104](https://github.com/fengyuanluo/InkForge/issues/104)) ([16d6f4b](https://github.com/fengyuanluo/InkForge/commit/16d6f4bb5b45edee3e1876c95e0783aea15a2f91))

## [0.7.2](https://github.com/fengyuanluo/InkForge/compare/v0.7.1...v0.7.2) (2026-07-15)


### 🐛 问题修复

* **desktop:** 修复更新日志渲染 ([#102](https://github.com/fengyuanluo/InkForge/issues/102)) ([2b75f25](https://github.com/fengyuanluo/InkForge/commit/2b75f25b1d08ecccbc4e9b7bee1e727b21fe24bf))

## [0.7.1](https://github.com/fengyuanluo/InkForge/compare/v0.7.0...v0.7.1) (2026-07-14)


### 🐛 问题修复

* **release:** 统一跨平台产物命名 ([#100](https://github.com/fengyuanluo/InkForge/issues/100)) ([56def22](https://github.com/fengyuanluo/InkForge/commit/56def22bf42fa660b0b1459929c7f928f1e02c09))

## [0.7.0](https://github.com/fengyuanluo/InkForge/compare/v0.6.2...v0.7.0) (2026-07-14)


### ✨ 新功能

* **desktop:** 支持应用内自动更新 ([#99](https://github.com/fengyuanluo/InkForge/issues/99)) ([bcd6eb9](https://github.com/fengyuanluo/InkForge/commit/bcd6eb94fe846c4237b89ffdad87d620ec7706b0))


### 🔧 杂项

* **build:** 迁移前端与桌面端构建至 Vite+ ([#97](https://github.com/fengyuanluo/InkForge/issues/97)) ([c77fd90](https://github.com/fengyuanluo/InkForge/commit/c77fd907ce9a0a55eac24e3fc49094c03c188a25))

## [0.6.2](https://github.com/fengyuanluo/InkForge/compare/v0.6.1...v0.6.2) (2026-07-13)


### 🐛 问题修复

* **agent:** 修复会话切换模型不生效 ([#91](https://github.com/fengyuanluo/InkForge/issues/91)) ([26ef7f3](https://github.com/fengyuanluo/InkForge/commit/26ef7f3beb202eb182b56ed483c144852be6d9c6))
* **agent:** 修复会话重连后流式事件丢失 ([#94](https://github.com/fengyuanluo/InkForge/issues/94)) ([018749c](https://github.com/fengyuanluo/InkForge/commit/018749caeea11f98d5f8405f17f7868949b3dbba))
* **agent:** 防止会话检查点泄露模型密钥 ([#92](https://github.com/fengyuanluo/InkForge/issues/92)) ([0342427](https://github.com/fengyuanluo/InkForge/commit/034242754890db39d2296f3b489c2c2317eb37e7))
* **mobile:** 修复移动端布局适配问题 ([#96](https://github.com/fengyuanluo/InkForge/issues/96)) ([f396b34](https://github.com/fengyuanluo/InkForge/commit/f396b34066577be9a9a3e5bbef4ace3192b7b1f4))
* **settings:** 锁定运行期间的智能体配置 ([#93](https://github.com/fengyuanluo/InkForge/issues/93)) ([6afd4b0](https://github.com/fengyuanluo/InkForge/commit/6afd4b0e9fa8c106917e8d3ec07f32255c30f7e4))


### ♻️ 代码重构

* **prompt-chains:** 重构提示词管理页面 ([#95](https://github.com/fengyuanluo/InkForge/issues/95)) ([73db522](https://github.com/fengyuanluo/InkForge/commit/73db52232f506edb9bda8e76156382aef4508310))


### 🔧 杂项

* **agent:** 限制子智能体委派与提问能力 ([#90](https://github.com/fengyuanluo/InkForge/issues/90)) ([9999283](https://github.com/fengyuanluo/InkForge/commit/999928376012548bfca968aab270f38e7bcd3a83))
* **models:** 优化模型选择器并移除Provider图标上传 ([#87](https://github.com/fengyuanluo/InkForge/issues/87)) ([436f761](https://github.com/fengyuanluo/InkForge/commit/436f761611ee57c67bcf0cdad72284b85a9fafaf))
* **providers:** 优化内置提供商选取、刷新与调用 ([#89](https://github.com/fengyuanluo/InkForge/issues/89)) ([0fe4188](https://github.com/fengyuanluo/InkForge/commit/0fe418852730254789473fdcd96993136f7dabc2))

## [0.6.1](https://github.com/fengyuanluo/InkForge/compare/v0.6.0...v0.6.1) (2026-07-11)


### 🐛 问题修复

* **backend:** 去重会话标题后台任务 ([#82](https://github.com/fengyuanluo/InkForge/issues/82)) ([afd9650](https://github.com/fengyuanluo/InkForge/commit/afd96506fff12d006383bedaae83c8273349a8c6))
* **background:** 修复孤儿后台任务无法自动清理的问题 ([#83](https://github.com/fengyuanluo/InkForge/issues/83)) ([643531d](https://github.com/fengyuanluo/InkForge/commit/643531d73f86a860832305651bdc03a829ba136b))
* **frontend:** 修复规则编辑区布局 ([#85](https://github.com/fengyuanluo/InkForge/issues/85)) ([025efad](https://github.com/fengyuanluo/InkForge/commit/025efad2f6ddf624b7d37242bfd180f8fa1ad4e2))
* **index:** 修复索引取消清理与轮询导致的性能问题 ([#86](https://github.com/fengyuanluo/InkForge/issues/86)) ([73fa08e](https://github.com/fengyuanluo/InkForge/commit/73fa08e0f2c7e8049058e085837a45feb5cfeb28))


### ♻️ 代码重构

* **agent:** 重构 mention XML 流转链路 ([#78](https://github.com/fengyuanluo/InkForge/issues/78)) ([28e7b16](https://github.com/fengyuanluo/InkForge/commit/28e7b16aeb6c9d8288cd2d27210f075883a5d0ac))
* **agent:** 重构 Skill 功能 ([#77](https://github.com/fengyuanluo/InkForge/issues/77)) ([97e1f5e](https://github.com/fengyuanluo/InkForge/commit/97e1f5e20083de7b2f1ca22073bbbd42314abe9c))
* **index:** 重构索引面板与进度展示 ([#80](https://github.com/fengyuanluo/InkForge/issues/80)) ([eff0886](https://github.com/fengyuanluo/InkForge/commit/eff0886281ac277ccc49e03ab6cba8c3ec0c2eb3))
* **summary:** 重构摘要生成面板与交互体验 ([#84](https://github.com/fengyuanluo/InkForge/issues/84)) ([8e16a19](https://github.com/fengyuanluo/InkForge/commit/8e16a19204ff9718fcf7a25b38719a80c9c2cf52))


### 📚 文档

* 更新README ([#79](https://github.com/fengyuanluo/InkForge/issues/79)) ([869b98c](https://github.com/fengyuanluo/InkForge/commit/869b98c248dd442c96165a47883b2ff011d697df))


### 🔧 杂项

* **frontend:** 适配角色与世界书移动端顶栏 ([#74](https://github.com/fengyuanluo/InkForge/issues/74)) ([1824117](https://github.com/fengyuanluo/InkForge/commit/1824117893de708fe7c802379021885236e2ea2b))
* **status-bar:** 添加索引进度展示 ([#81](https://github.com/fengyuanluo/InkForge/issues/81)) ([84f94c7](https://github.com/fengyuanluo/InkForge/commit/84f94c725854e42d1e3a80cff82c707ebe30b643))

## [0.6.0](https://github.com/fengyuanluo/InkForge/compare/v0.5.0...v0.6.0) (2026-07-07)


### ✨ 新功能

* **agent:** 添加角色工具与回滚支持 ([#70](https://github.com/fengyuanluo/InkForge/issues/70)) ([4d2bbf0](https://github.com/fengyuanluo/InkForge/commit/4d2bbf06bef79b9fd97f2be414c6a5b779c5c865))
* **characters:** 添加角色管理功能 ([#64](https://github.com/fengyuanluo/InkForge/issues/64)) ([1d1626a](https://github.com/fengyuanluo/InkForge/commit/1d1626a316c5bcd0471f54807ae29a1ee81df918))
* **frontend:** 添加全局状态栏 ([#71](https://github.com/fengyuanluo/InkForge/issues/71)) ([d584d56](https://github.com/fengyuanluo/InkForge/commit/d584d560a6e05747655a4538593da48eaee87fbe))


### ♻️ 代码重构

* **frontend:** 将仪表盘图表库替换为 Nivo ([#72](https://github.com/fengyuanluo/InkForge/issues/72)) ([3cbd4b7](https://github.com/fengyuanluo/InkForge/commit/3cbd4b7389e39bf80d26d7ac8a24a85ae1a39a05))


### 🔧 杂项

* **api:** 世界书改为项目强绑定 ([#73](https://github.com/fengyuanluo/InkForge/issues/73)) ([393add6](https://github.com/fengyuanluo/InkForge/commit/393add677c755ddd60bf1019ebd6110b75b462b3))
* **backend:** 添加 justfile 后端命令封装 ([#69](https://github.com/fengyuanluo/InkForge/issues/69)) ([d66b128](https://github.com/fengyuanluo/InkForge/commit/d66b1282ef7a4934a11827e793b894937f0cfc86))
* **backend:** 迁移类型检查到 ty ([#68](https://github.com/fengyuanluo/InkForge/issues/68)) ([d404696](https://github.com/fengyuanluo/InkForge/commit/d40469688379706a176958cf6407d747a8c6b85c))
* **frontend:** 添加 Oxfmt 格式化支持 ([#67](https://github.com/fengyuanluo/InkForge/issues/67)) ([40e2efd](https://github.com/fengyuanluo/InkForge/commit/40e2efd7890749378e76958d85a9da0819789fdf))
* **frontend:** 迁移前端检查到 Oxlint ([#66](https://github.com/fengyuanluo/InkForge/issues/66)) ([7c10648](https://github.com/fengyuanluo/InkForge/commit/7c10648bcd31ab6f71248e8af5aa4d0f7414ac51))

## [0.5.0](https://github.com/fengyuanluo/InkForge/compare/v0.4.9...v0.5.0) (2026-07-04)


### ✨ 新功能

* **agent:** 支持世界书条目与回滚 ([#59](https://github.com/fengyuanluo/InkForge/issues/59)) ([b02549d](https://github.com/fengyuanluo/InkForge/commit/b02549d8ab8dc050478f98d8e95601c95ade3295))
* **frontend:** 添加 PWA 支持实现可安装应用 ([#56](https://github.com/fengyuanluo/InkForge/issues/56)) ([bd623fb](https://github.com/fengyuanluo/InkForge/commit/bd623fb73c87733a58e3d521cf9f066bcc0ccde7))


### 🐛 问题修复

* **agent:** 修复 subagent 回滚状态恢复 ([#60](https://github.com/fengyuanluo/InkForge/issues/60)) ([b5fa608](https://github.com/fengyuanluo/InkForge/commit/b5fa60852a1031f9626e0fff201b719da77cb4c0))
* **frontend:** 修复 Agent 消息完成重新挂载的问题 ([#61](https://github.com/fengyuanluo/InkForge/issues/61)) ([10e2e53](https://github.com/fengyuanluo/InkForge/commit/10e2e53811853d2b26c1bcdec5dd1152a02f1223))
* **frontend:** 修复 Agent 消息流式展示顺序 ([#63](https://github.com/fengyuanluo/InkForge/issues/63)) ([9b4ee74](https://github.com/fengyuanluo/InkForge/commit/9b4ee74f4e0f0481cba5f5c021ca0b61aa06c0f9))
* **frontend:** 调整 Agent 工具消息展示 ([#62](https://github.com/fengyuanluo/InkForge/issues/62)) ([f6ccfbb](https://github.com/fengyuanluo/InkForge/commit/f6ccfbb2d853ac009a13def1b96d5cad1043cffa))


### 🔧 杂项

* 调整 Agent 会话命名与任务列表交互 ([#58](https://github.com/fengyuanluo/InkForge/issues/58)) ([741d2e3](https://github.com/fengyuanluo/InkForge/commit/741d2e369a37c11d28f3831fd5eb5d777b09ab46))

## [0.4.9](https://github.com/fengyuanluo/InkForge/compare/v0.4.8...v0.4.9) (2026-07-02)


### 🐛 问题修复

* **assistant:** 使用稳定的 diff section type ([#50](https://github.com/fengyuanluo/InkForge/issues/50)) ([27decdc](https://github.com/fengyuanluo/InkForge/commit/27decdcdf4bfe1fb6404d73a552fa1cc53958876))
* **frontend:** 修复 Agent 侧边栏模型图标显示 ([#54](https://github.com/fengyuanluo/InkForge/issues/54)) ([9eeaaff](https://github.com/fengyuanluo/InkForge/commit/9eeaaff74c83a8d492eeb8fd3aa096017a89804c))
* **frontend:** 对齐 Agent 工具消息注册 ([#55](https://github.com/fengyuanluo/InkForge/issues/55)) ([b7942f5](https://github.com/fengyuanluo/InkForge/commit/b7942f5cab56836dbeb3f837e4e6ad5deff373b3))


### 🔧 杂项

* **frontend:** 统一设置面板加载行为 ([#52](https://github.com/fengyuanluo/InkForge/issues/52)) ([798e8ad](https://github.com/fengyuanluo/InkForge/commit/798e8add8df5d24c93bbf0d1118049f6b4412ea4))
* **frontend:** 补齐前端界面 i18n 文案接入 ([#51](https://github.com/fengyuanluo/InkForge/issues/51)) ([7932bf7](https://github.com/fengyuanluo/InkForge/commit/7932bf7e4f3175746677f1be990164ca64e3bc24))
* **frontend:** 调整设置面板模型禁用态 ([#53](https://github.com/fengyuanluo/InkForge/issues/53)) ([86449ec](https://github.com/fengyuanluo/InkForge/commit/86449ece001aa8dbf210d322d19522ed81d8f620))


### 👷 CI/CD

* **release:** 修复每次 PR 都触发发版 ([#48](https://github.com/fengyuanluo/InkForge/issues/48)) ([5668036](https://github.com/fengyuanluo/InkForge/commit/5668036edb098c386ec8369867f21e21c9b0bd60))

## [0.4.8](https://github.com/fengyuanluo/InkForge/compare/v0.4.7...v0.4.8) (2026-07-01)


### 🔧 杂项

* **frontend:** 调整设置面板自动保存 ([#46](https://github.com/fengyuanluo/InkForge/issues/46)) ([a94d0eb](https://github.com/fengyuanluo/InkForge/commit/a94d0ebf7683e2b864c5ba3539ede0f38bce66e9))

## [0.4.7](https://github.com/fengyuanluo/InkForge/compare/v0.4.6...v0.4.7) (2026-07-01)


### 🐛 问题修复

* **desktop:** 修复本地后端启动 ([#43](https://github.com/fengyuanluo/InkForge/issues/43)) ([12440f7](https://github.com/fengyuanluo/InkForge/commit/12440f715495a2755c81a7be794426ca2cb7027b))

## [0.4.6](https://github.com/fengyuanluo/InkForge/compare/v0.4.5...v0.4.6) (2026-07-01)


### 🐛 问题修复

* **desktop:** 修复本地运行时安装 ([#41](https://github.com/fengyuanluo/InkForge/issues/41)) ([f77988b](https://github.com/fengyuanluo/InkForge/commit/f77988ba27449fb0708bfcce6395027f4e067ea3))

## [0.4.5](https://github.com/fengyuanluo/InkForge/compare/v0.4.4...v0.4.5) (2026-07-01)


### 👷 CI/CD

* **package:** 优化发布缓存复用 ([#39](https://github.com/fengyuanluo/InkForge/issues/39)) ([68f9542](https://github.com/fengyuanluo/InkForge/commit/68f954246c1e1f9307313cda7c8e8f6082be2f8b))

## [0.4.4](https://github.com/fengyuanluo/InkForge/compare/v0.4.3...v0.4.4) (2026-07-01)


### 🐛 问题修复

* **desktop:** 修复 Windows 构建样式解析 ([#37](https://github.com/fengyuanluo/InkForge/issues/37)) ([e837bb1](https://github.com/fengyuanluo/InkForge/commit/e837bb14ea17d2a3ef46b0de6d6a72590f3778a9))

## [0.4.3](https://github.com/fengyuanluo/InkForge/compare/v0.4.2...v0.4.3) (2026-07-01)


### 👷 CI/CD

* **release:** 等待 release PR 可合并 ([#35](https://github.com/fengyuanluo/InkForge/issues/35)) ([6105251](https://github.com/fengyuanluo/InkForge/commit/6105251aa84f173ca9eb998dd229e05e5f243ac2))

## [0.4.2](https://github.com/fengyuanluo/InkForge/compare/v0.4.1...v0.4.2) (2026-07-01)


### 🐛 问题修复

* **ci:** 修复桌面发布流程 ([#33](https://github.com/fengyuanluo/InkForge/issues/33)) ([9f100fc](https://github.com/fengyuanluo/InkForge/commit/9f100fc8c4ab75f09f5fd5262cfbe7ca66e62353))

## [0.4.1](https://github.com/fengyuanluo/InkForge/compare/v0.4.0...v0.4.1) (2026-07-01)


### 🐛 问题修复

* **ci:** 调整发布打包流程 ([#31](https://github.com/fengyuanluo/InkForge/issues/31)) ([f83451a](https://github.com/fengyuanluo/InkForge/commit/f83451a76225daa2c4d1669e93ef9f7f5309f52b))

## [0.4.0](https://github.com/fengyuanluo/InkForge/compare/v0.3.3...v0.4.0) (2026-07-01)


### ✨ 新功能

* **desktop:** 添加桌面端应用 ([#29](https://github.com/fengyuanluo/InkForge/issues/29)) ([77c7789](https://github.com/fengyuanluo/InkForge/commit/77c7789e322b3a7ee029c4837272bf8a7c10df28))

## [0.3.3](https://github.com/fengyuanluo/InkForge/compare/v0.3.2...v0.3.3) (2026-06-30)


### 🐛 问题修复

* **backend:** 完善后端分发构建与启动入口 ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* **backend:** 完善后端构建与分发流程 ([#27](https://github.com/fengyuanluo/InkForge/issues/27)) ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))
* **backend:** 完善后端构建与分发流程 ([#27](https://github.com/fengyuanluo/InkForge/issues/27)) ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))


### ♻️ 代码重构

* **backend:** 统一后台运行日志输出 ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))


### 📚 文档

* **readme:** 更新项目介绍与发布提示 ([86b3d77](https://github.com/fengyuanluo/InkForge/commit/86b3d77baff1a5cc5d57e1617fc6e619eb1090d0))

## [0.3.2](https://github.com/fengyuanluo/InkForge/compare/v0.3.1...v0.3.2) (2026-06-29)


### 🐛 问题修复

* **frontend:** 完善移动端适配 ([#25](https://github.com/fengyuanluo/InkForge/issues/25)) ([a971904](https://github.com/fengyuanluo/InkForge/commit/a971904f00466b53203aa87fb146330aad5e710a))

## [0.3.1](https://github.com/fengyuanluo/InkForge/compare/v0.3.0...v0.3.1) (2026-06-29)


### 🐛 问题修复

* **ci:** 等待 release PR 可合并后再自动合并 ([#23](https://github.com/fengyuanluo/InkForge/issues/23)) ([d868fc6](https://github.com/fengyuanluo/InkForge/commit/d868fc6647d0f5cd8097f3e19c55a4f1c8546233))

## [0.3.0](https://github.com/fengyuanluo/InkForge/compare/v0.2.6...v0.3.0) (2026-06-29)


### ✨ 新功能

* **frontend:** 补齐前端国际化文案并对齐英文翻译 ([#21](https://github.com/fengyuanluo/InkForge/issues/21)) ([59d4249](https://github.com/fengyuanluo/InkForge/commit/59d4249bfdfdb2b5867a789a7951e5812de8a011))

## [0.2.6](https://github.com/fengyuanluo/InkForge/compare/v0.2.5...v0.2.6) (2026-06-29)


### 🐛 问题修复

* **ci:** 同步 uv.lock 并修正后端包名 ([#19](https://github.com/fengyuanluo/InkForge/issues/19)) ([344bd82](https://github.com/fengyuanluo/InkForge/commit/344bd82c5ac43ad85203f8d09ad340e5e4d46e18))

## [0.2.5](https://github.com/fengyuanluo/InkForge/compare/v0.2.4...v0.2.5) (2026-06-29)


### 🐛 问题修复

* **ci:** 修复 release-please 未更新后端版本号及镜像版本 ([#17](https://github.com/fengyuanluo/InkForge/issues/17)) ([de2bbdc](https://github.com/fengyuanluo/InkForge/commit/de2bbdc611cfb2615bc5be1987d4a82066dcd6e9))

## [0.2.4](https://github.com/fengyuanluo/InkForge/compare/v0.2.3...v0.2.4) (2026-06-29)


### 🐛 问题修复

* **agent:** 移除子计划依赖并改用笔记大纲 ([#15](https://github.com/fengyuanluo/InkForge/issues/15)) ([da97a8b](https://github.com/fengyuanluo/InkForge/commit/da97a8be36256a814677a20d540f853713f496f5))

## [0.2.3](https://github.com/fengyuanluo/InkForge/compare/v0.2.2...v0.2.3) (2026-06-28)


### 🐛 问题修复

* **build:** 修正 electron-builder 配置并启用 changelog 作者显示 ([#13](https://github.com/fengyuanluo/InkForge/issues/13)) ([82532ee](https://github.com/fengyuanluo/InkForge/commit/82532ee37eb92e6965056b0e56c41c9a37fbbc8b))

## [0.2.2](https://github.com/fengyuanluo/InkForge/compare/v0.2.1...v0.2.2) (2026-06-28)


### 🐛 问题修复

* **ci:** 修复 Docker 推送 403 与版本号同步缺失 ([ed002f5](https://github.com/fengyuanluo/InkForge/commit/ed002f5e276402f5302675fa4ff6688c2acdc6a4))

## [0.2.1](https://github.com/fengyuanluo/InkForge/compare/v0.2.0...v0.2.1) (2026-06-28)


### 🐛 问题修复

* **test:** 移除引用已迁移路径与偶发卡死的失效测试 ([eb638df](https://github.com/fengyuanluo/InkForge/commit/eb638df74a1754c65351ec924098edabd7c15ebe))

## [0.2.0](https://github.com/fengyuanluo/InkForge/compare/v0.1.0...v0.2.0) (2026-06-28)


### ✨ 新功能

* 完善项目 README 文档 ([ca919a2](https://github.com/fengyuanluo/InkForge/commit/ca919a2f376937da1cd7aa8179a735bf45c8896c))


### 🐛 问题修复

* **ci:** 修复 release PR 合并命令参数解析 ([cf42194](https://github.com/fengyuanluo/InkForge/commit/cf421944b77747de1b4c78b8925621d85e74f461))
* **ci:** 修正 release-please manifest 配置结构 ([3bf931b](https://github.com/fengyuanluo/InkForge/commit/3bf931bdc53f244f01faf8115dca453e3232dd18))
* **ci:** 合并 release PR 前增加 checkout ([e1bf61a](https://github.com/fengyuanluo/InkForge/commit/e1bf61a01fc477a73076d77b433fd42113bf1c2f))
