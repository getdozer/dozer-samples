import { execSync } from 'child_process';
import path from 'path';

import {
  assertEndpointsWithRetry, initDozer,
} from '../helper';

const TEST_PATH = './connectors/snowflake';

describe('Connectors: Snowflake', async () => {
  beforeEach(async () => {
    const baseDir = path.join(__dirname, '../../');
    const fullPath = path.join(baseDir, TEST_PATH);
    process.chdir(fullPath);

    console.log(`Current directory: ${process.cwd()}`);

    execSync('rm -rf .dozer && rm -f dozer.lock', { stdio: 'inherit' });
  });

  it('should run and return API endpoints', async () => {
    const dozer = await initDozer();
    await assertEndpointsWithRetry();
    dozer.kill();
    console.log('Killed dozer snowflake');
  });
});
