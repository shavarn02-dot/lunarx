import { RegistrationWorkspace } from '@/components/registration-workspace'
import benchmarks from '../../data/outputs/benchmark_results.json'

export const dynamic = 'force-dynamic'

export default async function Page() {
  let online = false
  try {
    const response = await fetch('http://127.0.0.1:8000/api/health', {
      cache: 'no-store', signal: AbortSignal.timeout(1500),
    })
    online = response.ok
  } catch {}
  return <RegistrationWorkspace initialOnline={online} benchmark={benchmarks[0]} />
}
