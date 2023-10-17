import { execSync } from 'child_process';
import {
  assertEndpointsWithRetry, initDozer,
} from '../helper';

const TEST_PATH = './connectors/postgres';

describe('Connectors: Postgres', async () => {
  beforeEach(async () => {
    process.chdir('../../'); // go to root
    console.log(`Starting directory: ${process.cwd()}`);

    // Download init.sql and setup docker image
    execSync(`${__dirname}/initPostgres.sh`, { stdio: 'inherit' });

    process.chdir(TEST_PATH);
    execSync('rm -rf .dozer && rm -f dozer.lock', { stdio: 'inherit' });
  });

  it('should run and return API endpoints', async () => {
    const dozer = await initDozer();
    await assertEndpointsWithRetry();
    dozer.kill(9);
    console.log('Killed dozer postgres');
  });
});
