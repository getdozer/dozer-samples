import CodeBlock from '../components/CodeBlock';
import Guide from '../docs/Guide.mdx';
import { usePageView } from '../hooks/usePageView';

export function Home() {
  usePageView();
  return <Guide components={{
    code: function code(props) {
      console.log(props);
      return <CodeBlock language={props.className?.replace('language-', '')} content={props.children as string}></CodeBlock>
    },
    wrapper(props) {
      return <div className="markdown-body" style={{
        height: '100%',
        padding: '1rem',
      }} {...props} />;
    },
  }}/>;
}
