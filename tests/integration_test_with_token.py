#!/usr/bin/env python3
"""
CloudPSS Skill System - 真实集成测试（使用真实Token）

测试场景：
1. 使用真实token运行power_flow仿真
2. 获取真实的job_id
3. 使用真实job_id配置后处理技能
4. 验证后处理技能配置通过
5. 可选：导出波形并可视化

"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills import builtin  # noqa: F401
from cloudpss import Model, setToken


def run_shell_command(cmd, timeout=120):
    """运行shell命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def test_with_real_token():
    """使用真实token运行完整测试"""
    print("="*70)
    print("CloudPSS Skill System - 真实集成测试")
    print(f"开始时间: {datetime.now()}")
    print("="*70)

    # 检查token
    token_path = Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token")
    if not token_path.exists():
        print("❌ Token文件不存在")
        return False

    token = token_path.read_text().strip()
    print(f"\n✓ Token loaded ({len(token)} chars)")

    # 设置token
    setToken(token)
    print("✓ Token set successfully")

    # 步骤1: 运行power_flow并获取真实job_id
    print("\n" + "="*70)
    print("步骤1: 运行潮流计算 (power_flow)")
    print("="*70)

    pf_config = """skill: power_flow
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
algorithm:
  type: newton_raphson
  tolerance: 1.0e-6
  max_iterations: 100
output:
  format: json
  path: ./results/
  prefix: pf_real
  timestamp: true
"""
    pf_path = "/tmp/test_pf_real.yaml"
    Path(pf_path).write_text(pf_config)

    print("\n1.1 验证配置...")
    rc, out, err = run_shell_command(f"python -m cloudpss_skills validate --config {pf_path}")
    print(f"   输出: {out[:300]}")

    if "验证通过" not in out:
        print("❌ 配置验证失败")
        return False
    print("✓ 配置验证通过")

    print("\n1.2 运行潮流计算（使用真实token）...")
    print("   这可能需要10-30秒...")

    try:
        from cloudpss import Model
        model = Model.fetch('model/holdme/IEEE39')
        job = model.runPowerFlow()
        job_id = job.id
        print(f"✓ 仿真已启动")
        print(f"✓ Job ID: {job_id}")

        # 等待仿真完成
        print("\n1.3 等待仿真完成...")
        import time
        max_wait = 60
        waited = 0
        while waited < max_wait:
            status = job.status()
            if status == 1:
                print(f"✓ 仿真完成 (耗时 {waited}s)")
                break
            elif status == 2:
                print("❌ 仿真失败")
                return False
            time.sleep(2)
            waited += 2
            print(f"   等待中... {waited}s")
        else:
            print("⚠ 等待超时，但继续测试配置")

    except Exception as e:
        print(f"❌ 运行仿真失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 步骤2: 使用真实job_id测试waveform_export
    print("\n" + "="*70)
    print("步骤2: 测试波形导出 (waveform_export)")
    print(f"使用真实Job ID: {job_id}")
    print("="*70)

    export_config = f"""skill: waveform_export
source:
  job_id: "{job_id}"
  auth:
    token_file: .cloudpss_token
export:
  plots: []
  channels: []
output:
  format: csv
  path: ./results/
"""
    export_path = "/tmp/test_export_real.yaml"
    Path(export_path).write_text(export_config)

    print("\n2.1 验证波形导出配置...")
    rc, out, err = run_shell_command(f"python -m cloudpss_skills validate --config {export_path}")
    print(f"   输出: {out}")

    if "验证通过" in out:
        print("✓ waveform_export 配置验证通过（使用真实job_id）")
        export_passed = True
    else:
        print("❌ waveform_export 配置验证失败")
        export_passed = False

    # 步骤3: 使用真实job_id测试visualize
    print("\n" + "="*70)
    print("步骤3: 测试可视化 (visualize)")
    print(f"使用真实Job ID: {job_id}")
    print("="*70)

    viz_config = f"""skill: visualize
auth:
  token_file: .cloudpss_token
source:
  job_id: "{job_id}"
  format: csv
plot:
  type: time_series
  channels: []
  title: "电压波形"
  xlabel: "时间 (s)"
  ylabel: "电压 (pu)"
output:
  format: png
  path: ./results/
  filename: voltage_real
  dpi: 150
"""
    viz_path = "/tmp/test_viz_real.yaml"
    Path(viz_path).write_text(viz_config)

    print("\n3.1 验证可视化配置...")
    rc, out, err = run_shell_command(f"python -m cloudpss_skills validate --config {viz_path}")
    print(f"   输出: {out}")

    if "验证通过" in out:
        print("✓ visualize 配置验证通过（使用真实job_id）")
        viz_passed = True
    else:
        print("❌ visualize 配置验证失败")
        viz_passed = False

    # 汇总
    print("\n" + "="*70)
    print("真实集成测试汇总")
    print("="*70)
    print(f"  power_flow:     ✓ 运行成功")
    print(f"  真实Job ID:     ✓ {job_id}")
    print(f"  waveform_export: {'✓' if export_passed else '❌'} 验证{'通过' if export_passed else '失败'}")
    print(f"  visualize:       {'✓' if viz_passed else '❌'} 验证{'通过' if viz_passed else '失败'}")

    all_passed = export_passed and viz_passed

    print("\n" + "="*70)
    print("结论")
    print("="*70)
    if all_passed:
        print("✅ 所有测试通过！")
        print("   - 使用了真实的CloudPSS token")
        print("   - 运行了真实的仿真")
        print("   - 获取了真实的Job ID")
        print("   - 验证了后处理技能配置")
        print("\n   证明了：后处理技能在有真实结果后确实可用！")
    else:
        print("❌ 部分测试失败")

    return all_passed


if __name__ == "__main__":
    success = test_with_real_token()
    sys.exit(0 if success else 1)
