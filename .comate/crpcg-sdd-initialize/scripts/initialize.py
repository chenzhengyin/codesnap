#!/usr/bin/env python3
"""
CRPCG 项目初始化脚本

从公司仓库初始化项目的 AI 辅助开发环境。
"""

import argparse
import shutil
import tempfile
import subprocess
import sys
from pathlib import Path
from typing import List


# 仓库地址
REPO_URL = "http://gitea.crpcg.com/common-components/ai-coding-sdd.git"

# 需要创建的目录结构
DIRECTORY_STRUCTURE = {
    ".comate/rules": "目录",
    ".comate/references": "目录",
    ".comate/skills": "目录",
    ".comate/agents": "目录",
    ".comate/scripts": "目录",
    ".comate/templates": "目录",
    ".comate/mcp": "目录",
    "docs/references": "目录",
    "docs/references/tech-assets": "目录",
    "docs/requirements": "目录",
}

# 项目类型配置
PROJECT_TYPE_CONFIG = {
    "backend": {
        "name": "后端项目",
        "rules": ["git-workflow.mdr", "lang-java.mdr", "lang-sql.mdr", "quality.mdr", "security.mdr"],
        "references": ["crpcg-application-log-spec.md", "crpcg-idempotent-spec.md", "crpcg-integration-log-spec.md"],
        "technical_template": "technical.md",
    },
    "vue": {
        "name": "Vue项目",
        "rules": ["lang-vue-typescript.mdr", "git-workflow.mdr", "quality.mdr", "security.mdr"],
        "references": ["crpcg-rc-vue-spec.md"],
        "technical_template": "technical-frontend.md",
    },
    "react": {
        "name": "React项目",
        "rules": ["lang-react-typescript.mdr", "git-workflow.mdr", "quality.mdr", "security.mdr"],
        "references": [],
        "technical_template": "technical-frontend.md",
    },
    "react-native": {
        "name": "ReactNative项目",
        "rules": ["lang-react-typescript.mdr", "git-workflow.mdr", "quality.mdr", "security.mdr"],
        "references": ["crpcg-rc-rn-spec.md"],
        "technical_template": "technical-frontend.md",
    },
    "uniapp": {
        "name": "Uniapp项目",
        "rules": ["lang-vue-typescript.mdr", "git-workflow.mdr", "quality.mdr", "security.mdr"],
        "references": [],
        "technical_template": "technical-frontend.md",
    },
}


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="初始化 CRPCG 项目标准结构"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        required=True,
        help="项目根目录路径"
    )
    parser.add_argument(
        "--project-type",
        type=str,
        required=True,
        choices=list(PROJECT_TYPE_CONFIG.keys()),
        help="项目类型: backend, vue, react, react-native, uniapp"
    )
    parser.add_argument(
        "--repo-path",
        type=str,
        default="",
        help="已克隆的仓库路径，留空则自动克隆"
    )
    parser.add_argument(
        "--skip-clone",
        action="store_true",
        help="跳过克隆步骤（使用 --repo-path 指定的路径）"
    )
    return parser.parse_args()


def clone_repo(target_path: str) -> bool:
    """克隆仓库到指定路径"""
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, target_path],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"克隆仓库失败: {e.stderr}")
        return False


def merge_agents_md(project_root: Path, repo_agents_path: Path) -> bool:
    """
    合并 AGENTS.md 文件
    
    如果项目已有 AGENTS.md，在头部插入仓库中的新内容。
    如果不存在，直接复制。
    """
    project_agents = project_root / "AGENTS.md"
    
    if not repo_agents_path.exists():
        print("仓库中未找到 AGENTS.md")
        return False
    
    # 读取仓库内容，去除 BOM
    repo_content = repo_agents_path.read_text(encoding="utf-8-sig")
    
    if project_agents.exists():
        # 读取已有内容，去除 BOM
        existing_content = project_agents.read_text(encoding="utf-8-sig")
        
        # 检查是否已经是相同内容
        if existing_content == repo_content:
            print("AGENTS.md 内容相同，无需更新")
            return True
        
        # 在头部插入新内容
        merged_content = repo_content + "\n\n---\n\n# 项目自定义配置\n\n" + existing_content
        project_agents.write_text(merged_content, encoding="utf-8")
        print("已合并 AGENTS.md（仓库内容插入头部）")
    else:
        project_agents.write_text(repo_content, encoding="utf-8")
        print("已创建 AGENTS.md")
    
    return True


def copy_rules(
    project_root: Path,
    repo_path: Path,
    selected_rules: List[str]
) -> int:
    """
    复制规则文件到项目
    
    返回成功复制的文件数量
    """
    rules_dir = project_root / ".comate" / "rules"
    repo_rules_dir = repo_path / "rules"
    
    if not repo_rules_dir.exists():
        print("仓库中未找到 rules 目录")
        return 0
    
    copied_count = 0
    
    for rule_file in selected_rules:
        # 添加 .mdr 后缀（如果用户没提供）
        if not rule_file.endswith(".mdr"):
            rule_file = rule_file + ".mdr"
        
        src = repo_rules_dir / rule_file
        dst = rules_dir / rule_file
        
        if not src.exists():
            print(f"规则文件不存在: {rule_file}")
            continue
        
        if dst.exists():
            print(f"跳过已存在的规则文件: {rule_file}")
            continue
        
        shutil.copy2(src, dst)
        print(f"已复制规则文件: {rule_file}")
        copied_count += 1
    
    return copied_count


def copy_references(
    project_root: Path,
    repo_path: Path,
    selected_references: List[str]
) -> int:
    """
    复制引用文件到项目的 .comate/references 目录
    
    返回成功复制的文件数量
    """
    references_dir = project_root / ".comate" / "references"
    repo_references_dir = repo_path / "references"
    
    if not repo_references_dir.exists():
        print("仓库中未找到 references 目录")
        return 0
    
    copied_count = 0
    
    for ref_file in selected_references:
        src = repo_references_dir / ref_file
        dst = references_dir / ref_file
        
        if not src.exists():
            print(f"引用文件不存在: {ref_file}")
            continue
        
        if dst.exists():
            print(f"跳过已存在的引用文件: {ref_file}")
            continue
        
        shutil.copy2(src, dst)
        print(f"已复制引用文件: {ref_file}")
        copied_count += 1
    
    return copied_count


def copy_directory_contents(src_dir: Path, dst_dir: Path, description: str = "") -> int:
    """
    复制目录下的所有内容（包括子目录和文件）
    
    返回复制的文件/目录数量
    """
    if not src_dir.exists():
        print(f"源目录不存在: {src_dir}")
        return 0
    
    copied_count = 0
    
    # 确保目标目录存在
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    for item in src_dir.iterdir():
        dst_item = dst_dir / item.name
        
        if item.is_file():
            if dst_item.exists():
                print(f"跳过已存在的文件: {description}/{item.name}")
            else:
                shutil.copy2(item, dst_item)
                print(f"已复制文件: {description}/{item.name}")
                copied_count += 1
        elif item.is_dir():
            # 递归复制子目录
            sub_count = copy_directory_contents(item, dst_item, f"{description}/{item.name}")
            copied_count += sub_count
    
    return copied_count


def copy_file(src: Path, dst: Path, description: str = "") -> bool:
    """
    复制单个文件
    
    返回是否成功复制
    """
    if not src.exists():
        print(f"源文件不存在: {src}")
        return False
    
    if dst.exists():
        print(f"跳过已存在的文件: {description}")
        return False
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"已复制文件: {description}")
    return True


def create_directory_structure(project_root: Path) -> int:
    """
    创建目录结构
    
    返回新创建的目录数量
    """
    created_count = 0
    
    for dir_path in DIRECTORY_STRUCTURE.keys():
        full_path = project_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"已创建目录: {dir_path}")
            created_count += 1
        else:
            print(f"目录已存在，跳过: {dir_path}")
    
    return created_count


def main():
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    
    if not project_root.exists():
        print(f"项目根目录不存在: {project_root}")
        sys.exit(1)
    
    # 获取项目类型配置
    project_config = PROJECT_TYPE_CONFIG.get(args.project_type)
    if not project_config:
        print(f"未知的项目类型: {args.project_type}")
        sys.exit(1)
    
    repo_path = None
    should_cleanup = False
    
    try:
        # 获取仓库路径
        if args.repo_path:
            repo_path = Path(args.repo_path).resolve()
        else:
            # 创建临时目录并克隆
            repo_path = Path(tempfile.mkdtemp(prefix="ai-coding-sdd-"))
            should_cleanup = True
            
            print(f"正在克隆仓库到: {repo_path}")
            if not clone_repo(str(repo_path)):
                sys.exit(1)
        
        if not repo_path.exists():
            print(f"仓库路径不存在: {repo_path}")
            sys.exit(1)
        
        print(f"项目根目录: {project_root}")
        print(f"项目类型: {project_config['name']}")
        print(f"规则文件: {project_config['rules']}")
        print(f"引用文件: {project_config['references']}")
        
        print("\n=== 开始初始化 ===\n")
        
        # 1. 创建目录结构
        print("--- 创建目录结构 ---")
        create_directory_structure(project_root)
        
        # 2. 复制规则文件
        print("\n--- 复制规则文件 ---")
        copy_rules(project_root, repo_path, project_config['rules'])
        
        # 3. 复制 skills 目录内容
        print("\n--- 复制 skills 目录 ---")
        repo_skills = repo_path / "skills"
        project_skills = project_root / ".comate" / "skills"
        if repo_skills.exists():
            copy_directory_contents(repo_skills, project_skills, "skills")
        else:
            print("仓库中未找到 skills 目录")

        # 4. 复制 agents 目录内容
        print("\n--- 复制 agents 目录 ---")
        repo_agents = repo_path / "agents"
        project_agents = project_root / ".comate" / "agents"
        if repo_agents.exists():
            copy_directory_contents(repo_agents, project_agents, "agents")
        else:
            print("仓库中未找到 agents 目录")

        # 5. 复制 scripts 目录内容
        print("\n--- 复制 scripts 目录 ---")
        repo_scripts = repo_path / "scripts"
        project_scripts = project_root / ".comate" / "scripts"
        if repo_scripts.exists():
            copy_directory_contents(repo_scripts, project_scripts, "scripts")
        else:
            print("仓库中未找到 scripts 目录")

        # 6. 复制 templates 目录内容
        print("\n--- 复制 templates 目录 ---")
        repo_templates = repo_path / "templates"
        project_templates = project_root / ".comate" / "templates"
        if repo_templates.exists():
            copy_directory_contents(repo_templates, project_templates, "templates")
        else:
            print("仓库中未找到 templates 目录")

        # 7. 复制 mcp 目录内容
        print("\n--- 复制 mcp 目录 ---")
        repo_mcp = repo_path / "mcp"
        project_mcp = project_root / ".comate" / "mcp"
        if repo_mcp.exists():
            copy_directory_contents(repo_mcp, project_mcp, "mcp")
        else:
            print("仓库中未找到 mcp 目录")

        # 8. 复制引用文件
        print("\n--- 复制引用文件 ---")
        if project_config['references']:
            copy_references(project_root, repo_path, project_config['references'])
        else:
            print("当前项目类型无需复制引用文件")

        # 9. 复制根目录的文档文件
        print("\n--- 复制文档文件 ---")

        # 复制 business.md
        business_src = repo_path / "templates" / "business.md"
        business_dst = project_root / "docs" / "business.md"
        copy_file(business_src, business_dst, "docs/business.md")

        # 根据 technical_template 配置选择模板
        technical_template = project_config.get("technical_template", "technical.md")
        technical_src = repo_path / "templates" / technical_template
        technical_dst = project_root / "docs" / "technical.md"
        if technical_src.exists():
            copy_file(technical_src, technical_dst, f"docs/technical.md (from templates/{technical_template})")
        else:
            print(f"模板文件不存在: templates/{technical_template}")

        # 10. 复制 README.md 到项目根目录
        print("\n--- 复制 README.md ---")
        repo_readme = repo_path / "README.md"
        project_readme = project_root / "README.md"
        copy_file(repo_readme, project_readme, "README.md")

        # 11. 处理 AGENTS.md
        print("\n--- 处理 AGENTS.md ---")
        merge_agents_md(project_root, repo_path / "AGENTS.md")
        
        print("\n=== 初始化完成 ===\n")
        
    finally:
        # 清理临时目录
        if should_cleanup and repo_path and repo_path.exists():
            print("正在清理临时文件...")
            shutil.rmtree(repo_path, ignore_errors=True)


if __name__ == "__main__":
    main()
