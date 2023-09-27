import { usePageView } from '../hooks/usePageView';
import config from '../../dozer-config.yaml?raw';
import CodeBlock from '../components/CodeBlock';

export function Config() {
  usePageView();
  return <CodeBlock language='yaml' content={config}/>
}
