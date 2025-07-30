#!/usr/bin/env python3
"""
GitHub Repository Creation Script
================================

This script helps create the GitHub repository for the AutoGen SoM Teams project.
"""

import requests
import json
import os
import subprocess
import sys

def create_github_repo():
    """Create GitHub repository using GitHub API."""
    
    # Repository details
    repo_data = {
        "name": "autogen-som-teams",
        "description": "Microsoft AutoGen Assignment 0 - Society of Mind Framework with UserProxyAgent Integration. Advanced multi-agent system demonstrating hierarchical coordination with strategic human-in-the-loop functionality.",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "auto_init": False,
        "allow_squash_merge": True,
        "allow_merge_commit": True,
        "allow_rebase_merge": True,
        "delete_branch_on_merge": True
    }
    
    print("🚀 GitHub Repository Creation Helper")
    print("=" * 50)
    
    # Check if GitHub CLI is available
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub CLI detected!")
            return create_with_gh_cli(repo_data)
    except FileNotFoundError:
        pass
    
    # Manual creation instructions
    print("📋 Manual Repository Creation Required")
    print("-" * 40)
    print()
    print("Please follow these steps:")
    print()
    print("1. 🌐 Open your browser and go to:")
    print("   https://github.com/new")
    print()
    print("2. 📝 Fill in the repository details:")
    print(f"   Repository name: {repo_data['name']}")
    print(f"   Description: {repo_data['description']}")
    print("   Visibility: Public")
    print("   ❌ Do NOT initialize with README, .gitignore, or license")
    print()
    print("3. 🎯 Click 'Create repository'")
    print()
    print("4. 🚀 After creation, run this command to push your code:")
    print("   git push -u origin main")
    print()
    
    # Wait for user confirmation
    input("Press Enter after you've created the repository on GitHub...")
    
    # Try to push
    try:
        print("\n🚀 Attempting to push code to GitHub...")
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Successfully pushed to GitHub!")
            print(f"🌐 Repository URL: https://github.com/glohar1993/{repo_data['name']}")
            return True
        else:
            print(f"❌ Push failed: {result.stderr}")
            print("\n🔧 Troubleshooting:")
            print("1. Make sure you created the repository on GitHub")
            print("2. Check your GitHub authentication")
            print("3. Try running: git push -u origin main")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_with_gh_cli(repo_data):
    """Create repository using GitHub CLI."""
    try:
        print("🚀 Creating repository with GitHub CLI...")
        
        cmd = [
            'gh', 'repo', 'create', repo_data['name'],
            '--description', repo_data['description'],
            '--public',
            '--source', '.',
            '--push'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Repository created and code pushed successfully!")
            print(f"🌐 Repository URL: https://github.com/glohar1993/{repo_data['name']}")
            return True
        else:
            print(f"❌ GitHub CLI failed: {result.stderr}")
            print("Falling back to manual creation...")
            return False
            
    except Exception as e:
        print(f"❌ GitHub CLI error: {e}")
        return False

def verify_git_setup():
    """Verify git configuration."""
    try:
        # Check git config
        name_result = subprocess.run(['git', 'config', 'user.name'], 
                                   capture_output=True, text=True)
        email_result = subprocess.run(['git', 'config', 'user.email'], 
                                    capture_output=True, text=True)
        
        if name_result.returncode == 0 and email_result.returncode == 0:
            print(f"✅ Git configured for: {name_result.stdout.strip()} <{email_result.stdout.strip()}>")
            return True
        else:
            print("❌ Git not configured properly")
            return False
            
    except Exception as e:
        print(f"❌ Git configuration error: {e}")
        return False

def main():
    """Main function."""
    print("🤖 Microsoft AutoGen - Assignment 0: SoM Teams")
    print("GitHub Repository Creation Helper")
    print("=" * 60)
    
    # Verify git setup
    if not verify_git_setup():
        print("\n🔧 Please configure git first:")
        print("git config --global user.name 'Your Name'")
        print("git config --global user.email 'your.email@example.com'")
        return
    
    # Check current directory
    if not os.path.exists('.git'):
        print("❌ Not in a git repository. Please run from the project root.")
        return
    
    # Create repository
    success = create_github_repo()
    
    if success:
        print("\n🎉 SUCCESS! Your repository is now live on GitHub!")
        print("\n📊 Repository Features:")
        print("✅ Professional README with badges and documentation")
        print("✅ Complete Society of Mind framework implementation")
        print("✅ 12 specialized AI agents with UserProxyAgent integration")
        print("✅ 3 working scenarios with real-world applications")
        print("✅ Comprehensive documentation and guides")
        print("✅ Production-ready code with enterprise-grade quality")
        
        print("\n🎯 Next Steps:")
        print("1. Visit your repository: https://github.com/glohar1993/autogen-som-teams")
        print("2. Add repository topics for better discoverability")
        print("3. Star your own repository to show it's complete")
        print("4. Share it on LinkedIn and professional networks")
        
    else:
        print("\n🔧 Manual Steps Required:")
        print("1. Create repository at: https://github.com/new")
        print("2. Run: git push -u origin main")
        print("3. Verify at: https://github.com/glohar1993/autogen-som-teams")

if __name__ == "__main__":
    main()
