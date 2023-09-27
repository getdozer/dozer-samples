import { Box, useTheme } from "@mui/material";
import Prism from 'prismjs';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-yaml';
import 'prismjs/themes/prism-okaidia.min.css';
import CopyToClipboard from "react-copy-to-clipboard";
import { useEffect, useRef, useState } from "react";
import CopySuccessIcon from '../assets/action-copy-success.svg?react';
import CopyIcon from '../assets/action-copy.svg?react';

export default function CodeBlock(props: {
  language?: string;
  content: string;
}
) {
  const codeRef = useRef<HTMLElement>(null);
  const theme = useTheme();

  const [copy, setCopy] = useState(false);

  useEffect(() => {
    codeRef.current && Prism.highlightElement(codeRef.current);
  }, [props.content]);

  const className = `language-${props.language ? props.language : 'bash'}`;
  return (
    <pre style={{
      backgroundColor: theme.palette.background.paper,
      border: `1px solid ${theme.palette.grey[300]}`,
      borderRadius: '6px',
      padding: '18px',
      position: 'relative',
      userSelect: 'text',
      height: '100%',
      boxSizing: 'border-box',
      margin: '0',
    }}>
      <code className={className} ref={codeRef} style={{ whiteSpace: 'break-spaces' }}>
        {props.content}
      </code>
      <Box sx={() => ({
        position: 'absolute',
        right: '18px',
        top: '18px',
        cursor: 'pointer',
      })}>
        {
          copy
            ? <CopySuccessIcon width={20} height={20} title='copy_success' />
            : (
              <CopyToClipboard text={props.content} onCopy={() => {
                setCopy(true);
                setTimeout(() => {
                  setCopy(false);
                }, 2000);
              }}>
                <CopyIcon width={20} height={20} title='copy' />
              </CopyToClipboard>
            )

        }
      </Box>
    </pre>
  )
}
