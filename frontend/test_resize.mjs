import { chromium } from 'playwright'

const browser = await chromium.launch({ args: ['--no-sandbox'] })
const page = await browser.newPage()

async function fabRect() {
  return await page.evaluate(() => {
    const btn = document.querySelector('button[aria-label="Abrir chat com a Assistente Virtual"]')
    if (!btn) return null
    const r = btn.getBoundingClientRect()
    return { left: r.left, top: r.top, right: r.right, bottom: r.bottom, vw: window.innerWidth, vh: window.innerHeight }
  })
}

await page.setViewportSize({ width: 800, height: 900 })
await page.goto('http://localhost:5173/')
await page.waitForSelector('button[aria-label="Abrir chat com a Assistente Virtual"]')
let r1 = await fabRect()
console.log('At 800px width:', JSON.stringify(r1))
console.log('  distance from right edge:', r1.vw - r1.right, ' from bottom:', r1.vh - r1.bottom)

await page.screenshot({ path: '/tmp/claude-1000/-home-rodrigo--rea-de-trabalho-dalia-cakes-web/c64b0e81-30f8-46db-b69d-80ca90973f95/scratchpad/before_resize_800.png' })

// Resize above 1024
await page.setViewportSize({ width: 1600, height: 900 })
await page.waitForTimeout(300)
let r2 = await fabRect()
console.log('After resizing to 1600px width:', JSON.stringify(r2))
console.log('  distance from right edge:', r2.vw - r2.right, ' from bottom:', r2.vh - r2.bottom)

await page.screenshot({ path: '/tmp/claude-1000/-home-rodrigo--rea-de-trabalho-dalia-cakes-web/c64b0e81-30f8-46db-b69d-80ca90973f95/scratchpad/after_resize_1600.png' })

const consistent = Math.abs((r1.vw - r1.right) - (r2.vw - r2.right)) < 2 && Math.abs((r1.vh - r1.bottom) - (r2.vh - r2.bottom)) < 2
console.log(consistent ? 'PASS: FAB stayed pinned to corner after resize' : 'FAIL: FAB did NOT stay pinned to corner')

await browser.close()
