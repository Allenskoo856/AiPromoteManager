# AI Prompt Manager 项目结构

```
ai-prompt-manager/
├── backend/                 # 后端项目目录
│   ├── app/                # FastAPI 应用目录
│   │   ├── api/           # API 路由
│   │   ├── core/          # 核心配置
│   │   ├── crud/          # 数据库操作
│   │   ├── db/            # 数据库配置
│   │   ├── models/        # SQLAlchemy 模型
│   │   └── schemas/       # Pydantic 模型
│   ├── tests/             # 测试目录
│   ├── requirements.txt    # Python 依赖
│   └── main.py            # 入口文件
├── frontend/               # 前端项目目录
│   ├── public/            # 静态资源
│   ├── src/               # 源代码
│   │   ├── assets/       # 资源文件
│   │   ├── components/   # Vue 组件
│   │   ├── router/       # 路由配置
│   │   ├── store/        # Vuex 状态管理
│   │   ├── views/        # 页面视图
│   │   └── App.vue       # 根组件
│   ├── package.json      # npm 配置
│   └── vite.config.js    # Vite 配置
└── docker/                # Docker 配置目录
    ├── docker-compose.yml # Docker Compose 配置
    ├── backend.dockerfile # 后端 Docker 配置
    └── frontend.dockerfile# 前端 Docker 配置 