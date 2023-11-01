import { execSync } from 'child_process';
import path from 'path';
import {
  assertEndpointsWithRetry, initDozer,
} from '../helper';

const TEST_PATH = './connectors/mysql';

describe('Connectors: MySQL', async () => {
  beforeEach(async () => {
    process.chdir('../../'); // go to root
    console.log(`Starting directory: ${process.cwd()}`);

    // Download init.sql and setup docker image
    execSync(`${__dirname}/initMySQL.sh`, { stdio: 'inherit' });

    // navigate to test path
    const baseDir = path.join(__dirname, '../../');
    const fullPath = path.join(baseDir, TEST_PATH);
    process.chdir(fullPath);
    execSync('rm -rf .dozer && rm -f dozer.lock', { stdio: 'inherit' });
  });

  it('should run and return API endpoints', async () => {
    const dozer = await initDozer();
    await assertEndpointsWithRetry();
    dozer.kill(9);
    console.log('Killed dozer mysql');
  });
});
