import { execSync } from 'child_process';
import {
  assertEndpointsWithRetry, initDozer,
} from '../helper';

const TEST_PATH = './connectors/local-storage';

describe('Connectors: Local Storage', async () => {
  beforeEach(async () => {
    console.log(`Starting directory: ${process.cwd()}`);

    // Copy test data to local-storage connector
    execSync(`${__dirname}/init.sh`, { stdio: 'inherit' });

    process.chdir(TEST_PATH);
    execSync('rm -rf .dozer && rm -f dozer.lock', { stdio: 'inherit' });
  });

  it('should run and return API endpoints', async () => {
    const dozer = await initDozer();
    await assertEndpointsWithRetry();
    dozer.kill(9);
  });
});
