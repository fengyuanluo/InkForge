# AGENTS.md

本文件适用于整个仓库。若子目录以后出现更具体的 `AGENTS.md`，以距离目标文件最近的规则为准。

## 工作准则

- 用仓库事实、实时状态和运行结果说话，不猜测不存在的接口、文件或行为。
- 修改前先查看 `git status --short --branch`、相关实现、调用链和现有测试；目标未闭环前不开工。
- 保持改动最小、直接可用，不做无关重构，不引入只为未来假设服务的抽象。
- 简单文档或配置修改不运行测试；代码修改只运行覆盖关键路径的最小验证；跨模块或高风险修改再扩大验证范围。
- 未经用户明确要求，不派生子代理，不修改任务无关文件，不清理或覆盖他人的未提交改动。
- 不使用 `git reset --hard`、强制 checkout 等破坏性命令；不回退不属于当前任务的改动。
- 不提交密钥、Token、Cookie、个人数据、数据库、运行数据、日志或构建产物。
- 优先级：用户指令 > 本文件及更深层规则 > 运行态事实 > 静态文档与历史经验。

## 仓库与远端

- 官方仓库：`https://github.com/syrizelink/OpenFic`，本地远端名为 `upstream`，只允许 fetch。
- 二开仓库：`https://github.com/fengyuanluo/OpenFic`，本地远端名为 `origin`，承载开发与发布。
- `origin/main` 是二开稳定主分支；`upstream/main` 是官方基线，不创建长期镜像分支。
- 禁止向 `upstream` push。若远端配置与上述约定不一致，先停止并查明原因。
- `main` 禁止 rebase、force-push 和改写历史。仓库初始化完成后，所有业务修改通过短期分支和 PR 合入。

## 分支与提交

分支命名：

- `feat/<name>`：二开功能。
- `fix/<name>`：二开缺陷修复。
- `chore/<name>`：依赖、构建、文档或维护工作。
- `sync/upstream-vX.Y.Z`：合并官方稳定版本。
- `hotfix/<name>`：需要快速发布的生产修复。

日常开发：

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/<name>
```

- 一个提交只表达一个完整意图，遵循 `docs/develop/commit-conventions.md` 中的 Conventional Commits。
- 功能与修复 PR 默认 squash 合并；上游同步 PR 必须保留 merge commit，便于审计官方基线。
- 尚未共享的个人功能分支可以 rebase 到 `origin/main`；已共享分支先确认协作者状态。
- 能回馈官方的通用修复优先提交 upstream PR，减少二开长期差异。
- 提交前只暂存任务相关文件，并再次检查 staged diff。

## 同步官方更新

生产默认跟随官方 Release 标签，不直接追逐未发布的 `upstream/main`。只有明确需要尚未发布的官方修复时，才合并具体官方提交或 `upstream/main`。

```bash
git fetch upstream --prune --tags
git switch main
git pull --ff-only origin main
git switch -c sync/upstream-vX.Y.Z
git log --oneline main..upstream/main
git diff --stat main...upstream/main
git merge --no-ff vX.Y.Z
```

- 在同步分支解决冲突并完成跨端验证，再通过 PR 合入 `main`。
- 冲突处理必须理解双方行为；不得机械选择 ours/theirs，不得丢弃二开功能或官方迁移。
- 开启 `rerere` 复用已验证的重复冲突解决方案，但仍需复核结果。
- 禁止 `git push --tags`。只推送明确创建的二开标签。
- 二开标签使用 `custom-v<官方版本>.<序号>`，例如 `custom-v0.10.0.1`，避免触发官方仅监听 `v*` 的发布工作流。
- 每次同步在 PR 或发布说明中记录官方标签/SHA、冲突文件、验证结果和不兼容项。

## 项目结构

### 根目录

- `README.md`、`README_EN.md`：项目入口与使用说明。
- `Dockerfile`：先构建前端，再将产物放入 FastAPI 镜像；运行数据挂载到 `/data`。
- `.github/workflows/`：PR 检查、打包检查、官方 Release 与多平台打包流程。
- `release-please-config.json`、`.release-please-manifest.json`、`CHANGELOG.md`：官方版本发布元数据。非发布任务不要修改。
- `docs/develop/`：仓库级开发约定。

### `backend/`

Python 3.12-3.13、FastAPI、SQLAlchemy/SQLModel、Alembic、LangGraph 后端。

- `app/main.py`：应用生命周期、路由、Socket.IO、静态前端和后台服务入口。
- `app/api/routers/`：HTTP 路由；`app/api/schemas/`：请求与响应模型；`app/api/middleware/`：API 中间件。
- `app/agent_runtime/`：Agent 图、运行器、工具、会话、上下文、持久化和恢复逻辑。
- `app/background/`：后台任务与运行时监管。
- `app/audit/`：审计上下文、队列和存储访问。
- `app/core/`：跨领域基础类型、错误、加密、存储和文本处理。
- `app/models/`：模型提供商、内置模型和注册逻辑。
- `app/prompts/`：内置及自定义 Agent Prompt 加载。
- `app/skills/`：内置写作 Skill 定义与加载。
- `app/retrieval/`、`app/memory/`：索引、检索、摘要与记忆处理。
- `app/storage/models/`：数据库模型；`repos/`：数据访问；`services/`：业务服务。
- `app/storage/migrations/versions/`：当前 Alembic 迁移；`legacy/`：历史迁移，不得修改已发布迁移。
- `tests/`：按后端领域组织的 pytest 测试。
- `pyproject.toml`、`uv.lock`：依赖、工具与锁文件；`justfile`：常用开发命令；`hatch_build.py`：Python 包构建时的前端集成。

### `frontend/`

React 19、TypeScript、Vite Plus、TanStack Query、Zustand、Tiptap 前端。

- `src/main.tsx`、`src/App.tsx`：启动、初始化与应用根组件。
- `src/features/`：按业务领域组织页面、组件、hooks、store 和局部 API；新增业务代码优先放入对应 feature。
- `src/components/`：真正跨业务复用的 UI 与编辑器组件，不放单一页面专用组件。
- `src/lib/`：API 客户端、Socket、运行时配置、类型辅助和纯工具。
- `src/routes/`、`src/stores/`、`src/hooks/`：全局路由、状态和通用 hooks。
- `src/i18n/`：中英文文案；新增可见文本必须同步 `zh-CN` 与 `en`。
- `src/styles/`：全局 token、基础样式、动画和工具样式。
- `src/pwa/`、`public/`：PWA 注册与静态资源。
- `e2e/`：Playwright 关键路径测试；`patches/`：pnpm 依赖补丁；`scripts/`：构建辅助脚本。
- `package.json`、`pnpm-lock.yaml`：前端脚本和锁文件。

### `desktop/`

Electron 桌面壳，负责安装/启动本地后端、数据目录、备份、更新和原生窗口。

- `src/main/`：Electron 主进程、窗口、IPC、后端进程、数据与更新管理。
- `src/main/runtime/`：Python/OpenFic 运行时下载、安装、启动和归档处理。
- `src/preload/`：受控的渲染进程桥接。
- `src/shared/`：主进程、preload 与 UI 共享的 IPC 和配置类型。
- `src/ui/`：桌面安装与管理界面，不是主 Web 应用界面。
- `resources/`：桌面打包资源；`scripts/`：开发、打包和本地更新脚本；`tests/`：桌面运行时测试。
- `electron-builder.yml`：正式打包配置；`package.json`、`pnpm-lock.yaml`：桌面依赖和脚本。

## 修改边界

- 优先延用现有模块和接口，不创建平行实现。新抽象必须减少真实复杂度或重复。
- Prompt、Agent、Skill 定制优先使用现有 custom 能力和持久化配置；只有产品默认行为确需变化时才修改 builtin。
- API 修改应沿现有 router -> service/repo 分层，并同步 Pydantic schema、前端类型/API 客户端及相关测试。
- 数据模型修改必须新增 Alembic 迁移，兼容已有 `/data`；禁止改写已发布迁移，升级验证前先备份真实数据副本。
- 前端业务逻辑留在对应 `features` 中；共享组件不得依赖具体业务 feature。
- Electron IPC 修改必须同步 `main`、`preload`、`shared` 和消费端类型，保持上下文隔离。
- 前端会被 Web、Docker、Python wheel 和桌面端共同消费；任何前端构建或运行时改动都要评估桌面端。
- 锁文件只在依赖声明实际变化时由对应包管理器更新，禁止手工编辑。
- 不提交 `data/`、`.env`、`*.db`、`node_modules/`、`dist/`、`frontend_dist/`、桌面打包目录、缓存和临时诊断文件。
- 不在普通功能提交中修改三端版本号、Release Please 配置或官方发布工作流。

## 验证规则

- 文档、注释和纯仓库配置：检查 diff 即可，不运行应用测试。
- 后端窄改动：在 `backend/` 运行目标 pytest；涉及公共类型或入口时再运行 Ruff 与 ty。
- 前端窄改动：在 `frontend/` 运行受影响检查；提交前至少保证 `format:check`、`lint`、`type-check` 或 `build` 中与改动相关的部分通过。
- 桌面窄改动：在 `desktop/` 运行 `lint`、`type-check`，涉及构建链时运行 `build`。
- 数据迁移、Agent 会话、Socket、后台任务和打包属于高风险路径，必须增加对应回归验证。
- 官方同步、跨端接口、依赖或构建修改：执行 `.github/workflows/pr-check.yml` 与 `package-check.yml` 所覆盖的相关完整检查。
- Playwright E2E 只用于用户关键路径或跨层行为，不因简单改动扩充测试矩阵。
- 验证失败先定位实现问题，不通过降低断言、跳过测试或扩大容错来掩盖缺陷。

常用命令：

```bash
# backend
cd backend
uv sync --frozen
uv run pytest <target>
uv run ruff check .
uv run ty check app
uv build

# frontend
cd frontend
pnpm install --frozen-lockfile
pnpm format:check
pnpm lint
pnpm type-check
pnpm build

# desktop（先安装 frontend 依赖）
cd desktop
pnpm install --frozen-lockfile
pnpm lint
pnpm type-check
pnpm build
```

## 交付检查

- 复查 `git status --short --branch` 和 `git diff --check`。
- 确认只暂存任务相关文件，提交信息准确描述行为。
- 报告实际运行的验证及其结果；未运行的测试明确说明原因。
- 推送后核对本地 `HEAD`、`origin/<branch>` 和 GitHub 远端 SHA。
- 保持工作树干净；删除任务产生且不应保留的临时文件。
