"""
快速驗證腳本
檢查所有核心模組是否正常運作
"""

import sys
import os

# 加入父目錄到路徑，以便導入 lib 模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """測試所有模組導入"""
    print("=" * 50)
    print("測試模組導入...")
    print("=" * 50)
    
    tests = [
        ("lib.config", "Config 設定模組"),
        ("lib.pdf_processor", "PDF 處理模組"),
        ("lib.image_cleaner_lama", "Lama Cleaner 模組"),
        ("lib.ocr_opensource", "EasyOCR 模組"),
        ("lib.pptx_generator", "PPTX 生成模組"),
    ]
    
    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"✓ {description:20s} - 正常")
        except Exception as e:
            print(f"✗ {description:20s} - 錯誤: {e}")
            return False
    
    return True

def test_config():
    """測試設定模組"""
    print("\n" + "=" * 50)
    print("測試設定模組...")
    print("=" * 50)
    
    try:
        from lib import config
        
        print(f"圖片生成模型: {config.MODEL_IMAGE_GEN}")
        print(f"OCR 模型: {config.MODEL_OCR}")
        print(f"最大重試次數: {config.MAX_RETRIES}")
        print(f"重試延遲: {config.RETRY_DELAYS}")
        
        # 驗證模型名稱
        assert config.MODEL_IMAGE_GEN == "gemini-2.0-flash", "圖片生成模型名稱錯誤"
        assert config.MODEL_OCR == "gemini-2.0-flash", "OCR 模型名稱錯誤"
        
        print("✓ 設定模組驗證通過")
        return True
        
    except Exception as e:
        print(f"✗ 設定模組錯誤: {e}")
        return False

def test_api_key():
    """測試 API Key"""
    print("\n" + "=" * 50)
    print("測試 API Key...")
    print("=" * 50)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("✗ 找不到 GEMINI_API_KEY")
        print("  請在 .env 檔案中設定 GEMINI_API_KEY")
        return False
    
    if len(api_key) < 20:
        print("✗ API Key 似乎太短，可能無效")
        return False
    
    print(f"✓ API Key 已設定 (長度: {len(api_key)})")
    return True

def test_main_programs():
    """測試主程式"""
    print("\n" + "=" * 50)
    print("測試主程式...")
    print("=" * 50)
    
    programs = [
        ("main", "CLI 主程式"),
        ("gui", "GUI 主程式"),
    ]
    
    for module_name, description in programs:
        try:
            __import__(module_name)
            print(f"✓ {description:20s} - 可導入")
        except Exception as e:
            print(f"✗ {description:20s} - 錯誤: {e}")
            return False
    
    return True

def main():
    """執行所有測試"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║  NotebookLM PDF 轉 PPTX - 快速驗證腳本        ║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    results = []
    
    # 執行測試
    results.append(("模組導入", test_imports()))
    results.append(("設定模組", test_config()))
    results.append(("API Key", test_api_key()))
    results.append(("主程式", test_main_programs()))
    
    # 總結
    print("\n" + "=" * 50)
    print("測試總結")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ 通過" if passed else "✗ 失敗"
        print(f"{test_name:15s}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 所有測試通過！程式已準備就緒。")
        print("\n下一步：")
        print("  - 執行 CLI 版本: python main.py")
        print("  - 執行 GUI 版本: python gui.py")
        print("  - 查看測試指南: README_TEST.md")
        return 0
    else:
        print("\n⚠️  部分測試失敗，請檢查上述錯誤訊息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
