import { NextResponse } from "next/server"
import { getLogger } from "@/lib/logger"

// Vercel Cron Job endpoint
// Configure in vercel.json with: { "crons": [{ "path": "/api/cron", "schedule": "*/5 * * * *" }] }
export async function GET() {
  const logger = getLogger()

  try {
    logger.log("INFO", "Vercel Cron Job 触发")

    // 调用邮件处理API
    const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000"}/api/process-emails`)
    const result = await response.json()

    logger.log("INFO", "Vercel Cron Job 执行完成")

    return NextResponse.json({
      success: true,
      message: "Cron job executed",
      result,
    })
  } catch (error: any) {
    logger.log("ERROR", `Vercel Cron Job 执行失败: ${error.message}`)
    return NextResponse.json({ success: false, error: error.message }, { status: 500 })
  }
}
