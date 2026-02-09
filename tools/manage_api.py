"""
API Key 管理工具
"""

import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def update_api_key():
    """更新 API Key"""
    
    console.print("\n[bold cyan]Gemini API Key 管理工具[/bold cyan]\n")
    
    # 顯示當前 API Key
    env_path = ".env"
    current_key = ""
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    current_key = line.split('=', 1)[1].strip()
                    break
    
    if current_key:
        masked_key = current_key[:10] + "..." + current_key[-4:] if len(current_key) > 14 else current_key
        console.print(f"[yellow]當前 API Key:[/yellow] {masked_key}")
    else:
        console.print("[yellow]未設定 API Key[/yellow]")
    
    console.print("\n[cyan]請輸入新的 API Key：[/cyan]")
    console.print("[dim]（從 https://aistudio.google.com/app/apikey 取得）[/dim]")
    
    new_key = Prompt.ask("\nAPI Key", password=True)
    
    if not new_key or len(new_key) < 20:
        console.print("[red]✗ API Key 似乎無效（太短）[/red]")
        return False
    
    # 更新 .env 檔案
    try:
        with open(env_path, 'w') as f:
            f.write(f"GEMINI_API_KEY={new_key}\n")
        
        console.print("\n[bold green]✓ API Key 已更新！[/bold green]")
        console.print("\n[cyan]下一步：[/cyan]")
        console.print("  1. 測試新的 API Key：python verify.py")
        console.print("  2. 執行轉換：python convert.py \"PDF路徑\"")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ 更新失敗: {e}[/red]")
        return False

def test_api_key():
    """測試 API Key 是否有效"""
    
    console.print("\n[bold cyan]測試 API Key[/bold cyan]\n")
    
    try:
        from dotenv import load_dotenv
        from google import genai
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            console.print("[red]✗ 找不到 API Key[/red]")
            return False
        
        console.print("[yellow]測試連接中...[/yellow]")
        
        # 測試 API
        client = genai.Client(api_key=api_key)
        
        # 簡單的測試請求
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents='Hello'
        )
        
        console.print("[bold green]✓ API Key 有效！[/bold green]")
        console.print(f"[dim]回應: {response.text[:50]}...[/dim]")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ API Key 測試失敗: {e}[/red]")
        console.print("\n[yellow]可能原因：[/yellow]")
        console.print("  1. API Key 無效")
        console.print("  2. 已達配額限制")
        console.print("  3. 網路連接問題")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_api_key()
    else:
        console.print("\n[bold]選擇操作：[/bold]")
        console.print("  1. 更新 API Key")
        console.print("  2. 測試當前 API Key")
        console.print("  3. 離開")
        
        choice = Prompt.ask("\n請選擇", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            update_api_key()
        elif choice == "2":
            test_api_key()
        else:
            console.print("再見！")
