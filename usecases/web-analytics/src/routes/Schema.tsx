import schema from '../../schema.json?raw';
import CodeBlock from '../components/CodeBlock';
import { usePageView } from '../hooks/usePageView';

export function Schema() {
  usePageView();
  return <CodeBlock language='json' content={schema}/>
}
