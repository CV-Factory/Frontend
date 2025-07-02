<script lang="ts">
  import '$lib/i18n'; // Import to initialize
  import { onMount } from 'svelte';
  import { _ } from 'svelte-i18n';
  import { browser } from '$app/environment';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  const IS_LOCAL = browser && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
  const API_BASE_URL = IS_LOCAL ? 'http://localhost:8001' : 'https://cvfactory-server-627721457878.asia-northeast3.run.app';

  let jobUrl = '';
  let userPrompt = '';
  let generatedResume = '';
  let statusMessage = '';
  let isLoading = false;
  let eventSource: EventSource | null = null;
  let isSidebarOpen = false;

  const defaultPromptTextKo = `채용 공고 내용과 다음 사용자 프롬프트를 기반으로 자기소개서를 작성해 주세요.
    자기소개서는 한국어로, 전문적이고 회사와 직무에 맞춰 작성되어야 합니다.
    사용자 프롬프트에서 관련 있는 기술과 경험을 강조하고, 이를 채용 공고의 요구 사항과 연결해야 합니다.

    회사가 마주한 문제는 무엇이고,
    내가 가진 역량과 경험은 무엇인지,
    따라서 내가 회사의 그 문제를 어떤 식으로 해결 할 수 있는지를
    수치를 들어서 두괄식으로 기술해주세요.

    어투는 자신감 있고 열정적이어야 합니다.
    단순히 기술을 나열하는 것이 아니라 사용자 프롬프트를 자기소개서에 자연스럽게 통합해야 합니다.
    만약 사용자 프롬프트가 제공되지 않았다면, 채용 공고 내용만을 기반으로 자기소개서를 생성하되, 
    사용자가 자신의 특정 경험을 추가해야 할 부분을 '여기에 경험을 추가하세요'처럼 명시적으로 언급하지 않고, 
    자기소개서 내용 안에서 미묘하게 암시하도록 작성해 주세요.`;

  const defaultPromptTextEn = `Using the job posting details and the following user prompt, write a cover letter. The cover letter should be written in Korean, be professional, and tailored to the company and role. Emphasize the relevant skills and experiences from the user prompt and link them to the requirements of the job posting.

    1) What problem the company is facing,
    2) What competencies and experiences I have,
    3) How I can solve that problem for the company, described top-down with numbers and concrete figures where possible.

    Use a confident and passionate tone. Instead of simply listing skills, naturally weave the user prompt into the cover letter. If a user prompt is not provided, generate the cover letter based only on the job posting, subtly implying where the user should insert their own experience without explicitly saying things like 'Add your experience here'.`;

  onMount(() => {
    // Redirect logic
    if (browser && !$page.params.lang && window.navigator.language.startsWith('ko')) {
      goto('/ko', { replaceState: true });
    }

    const isKoreanPage = window.location.pathname.startsWith('/ko');
    userPrompt = isKoreanPage ? defaultPromptTextKo : defaultPromptTextEn;
  });

  function requestNotificationPermission() {
    return new Promise((resolve) => {
      if (!('Notification' in window)) {
        resolve(false);
      }
      if (Notification.permission === 'granted') {
        resolve(true);
      }
      if (Notification.permission !== 'denied') {
        Notification.requestPermission().then((permission) => {
          resolve(permission === 'granted');
        });
      } else {
        resolve(false);
      }
    });
  }

  function showBrowserNotification(title: string, body: string, onClickCallback?: () => void) {
    requestNotificationPermission().then((granted) => {
      if (granted) {
        const notification = new Notification(title, { body });
        notification.onclick = () => {
          window.focus();
          if (onClickCallback) {
            onClickCallback();
          }
          notification.close();
        };
      }
    });
  }

  function startTaskStreaming(taskId: string) {
    isLoading = true;
    let initialMessage = '자기소개서 생성을 시작합니다... 잠시만 기다려 주세요.';
    if ('Notification' in window && Notification.permission !== 'granted') {
      initialMessage += ' 브라우저 알림을 허용하시면 작업 완료 시 알려드립니다.';
    }
    statusMessage = initialMessage;
    generatedResume = '';

    if (eventSource) {
      eventSource.close();
    }

    eventSource = new EventSource(`${API_BASE_URL}/stream-task-status/${taskId}`);

    eventSource.onopen = function () {
      statusMessage = '서버와 연결되었습니다. 작업 진행 상황을 곧 받아옵니다...';
    };

    eventSource.onmessage = function (event) {
      try {
        const data = JSON.parse(event.data);
        let statusText;
        if (data.current_step) {
          if (data.status === 'STARTED') {
            statusText = data.current_step;
          } else {
            statusText = `${data.current_step} (상태: ${data.status})`;
          }
        } else {
          statusText = data.status;
        }
        statusMessage = `진행 상황: ${statusText}`;

        if (data.status === 'SUCCESS') {
          isLoading = false;
          let coverLetterText = '';
          if (typeof data.result === 'string') {
            coverLetterText = data.result;
          } else if (data.result && typeof data.result === 'object' && data.result.cover_letter_text) {
            coverLetterText = data.result.cover_letter_text;
          }

          if (coverLetterText) {
            generatedResume = coverLetterText;
            statusMessage = '자기소개서 생성이 완료되었습니다!';
            showBrowserNotification('자기소개서 생성 완료!', '자기소개서가 성공적으로 생성되었습니다!', () => {
              document.getElementById('generated_resume')?.focus();
            });
          } else {
            statusMessage = '생성된 자기소개서 내용이 비어있습니다.';
          }
          eventSource?.close();
        } else if (['FAILURE', 'ERROR_INTERNAL', 'ERROR_SETUP', 'ERROR_STREAM', 'ERROR_SERIALIZATION', 'ERROR_UNEXPECTED_STREAM'].includes(data.status)) {
          isLoading = false;
          let errorMessage = '자기소개서 생성에 실패했습니다.';
          if (data.result && data.result.error) {
            errorMessage += ` 오류: ${data.result.error}`;
          } else if (data.result && typeof data.result === 'string') {
            errorMessage += ` 오류: ${data.result}`;
          } else if (data.message) {
            errorMessage = data.message;
          }
          const currentStepInfo = data.current_step ? ` (단계: ${data.current_step})` : '';
          statusMessage = errorMessage + currentStepInfo;
          showBrowserNotification('자기소개서 생성 실패', errorMessage.replace(/\\n/g, ' ') + currentStepInfo);
          eventSource?.close();
        }
      } catch (e) {
        console.error('Error parsing SSE message or updating UI:', e, 'Raw data:', event.data);
        statusMessage = '데이터 처리 중 오류가 발생했습니다.';
      }
    };

    eventSource.onerror = function (err) {
      console.error('EventSource failed:', err);
      isLoading = false;
      statusMessage = '서버와 연결 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
      eventSource?.close();
    };
  }

  async function generateResume() {
    if (!jobUrl.trim()) {
      alert('채용 공고 URL을 입력해주세요.');
      return;
    }

    isLoading = true;
    statusMessage = '자기소개서 생성 요청 중...';
    generatedResume = '';

    const payload = {
      job_posting_url: jobUrl.trim(),
      user_prompt: userPrompt.trim() || null,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errData = await response.json();
        let detailMessage = '알 수 없는 오류';
        if (errData && errData.detail) {
            if (typeof errData.detail === 'string') {
                detailMessage = errData.detail;
            } else if (Array.isArray(errData.detail) && errData.detail.length > 0 && errData.detail[0].msg) {
                detailMessage = errData.detail.map((d: any) => `${d.loc.join('.')  } - ${  d.msg}`).join(', ');
            } else if (typeof errData.detail === 'object') {
                detailMessage = JSON.stringify(errData.detail);
            }
        }
        throw new Error(detailMessage);
      }

      const data = await response.json();
      if (data.task_id) {
        statusMessage = `작업이 시작되었습니다 (ID: ${data.task_id}). 잠시 후 결과가 표시됩니다.`;
        startTaskStreaming(data.task_id);
      } else {
        throw new Error('서버에서 작업 ID를 반환하지 않았습니다.');
      }
    } catch (error: any) {
      isLoading = false;
      statusMessage = `자기소개서 생성 요청에 실패했습니다: ${error.message}`;
      generatedResume = `오류로 인해 자기소개서를 생성할 수 없습니다: ${error.message}`;
    }
  }
</script>

<svelte:head>
  <title>{$_('page_title')}</title>
  <link rel="canonical" href="https://cvfactory.dev/">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content={$_('meta_description')}>
  <meta name="keywords" content={$_('meta_keywords')}>
</svelte:head>

<header>
  <div class="header-title" on:mouseenter={() => isSidebarOpen = true}>{$_('header_title')}</div>
</header>

<div class="main-container" on:mouseleave={() => isSidebarOpen = false}>
  <aside class="sidebar" class:open={isSidebarOpen}>
    <!-- Sidebar content goes here -->
    <p>Sidebar</p>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </aside>

  <main>
    <slot {userPrompt} />
  </main>
</div>

<style>
  :global(html) {
    height: 100%;
  }
  :global(body) {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow-x: hidden;
  }
  :global(*) {
    box-sizing: border-box;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    padding: 0 15px;
    border-bottom: 1px solid #eee;
  }

  .main-container {
    display: flex;
    flex: 1;
    overflow: auto; /* Allows content to scroll if it overflows */
  }

  .sidebar {
    width: 250px;
    background-color: #f4f4f4;
    padding: 20px;
    height: 100%; /* Make sidebar full height of the container */
    overflow-y: auto; /* Allow sidebar to scroll if content is long */
    transition: margin-left 0.3s ease-in-out;
    margin-left: -290px; /* (width)250px + (padding)40px */
  }

  .sidebar.open {
	  margin-left: 0;
  }

  main {
    flex: 1;
    padding: 1rem;
    height: 100%;
    overflow-y: auto; /* Allow main content to scroll */
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1 {
    text-align: center;
    margin-bottom: 20px;
    line-height: 1.2;
  }

  .prompt-container {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 20px;
  }

  .left-column {
    flex: 1;
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .right-column {
    flex: 1.5;
    min-width: 300px;
  }

  .chat-box {
    width: 100%;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  textarea {
    width: 100%;
    border: none;
    font-size: 16px;
    outline: none;
    resize: none;
    overflow-y: auto;
    background-color: white;
  }
  
  .small-prompt textarea {
      min-height: 50px;
      margin-bottom: 10px;
  }

  #prompt {
      height: 100%;
      box-sizing: border-box;
  }
  
  .large-prompt {
      min-height: 490px;
  }

  .large-prompt > div {
    display: flex;
    flex-direction: column;
    flex: 1;
    height: 100%;
  }

  .large-textarea {
    flex: 1;
    min-height: 350px;
    margin-bottom: 10px;
  }

  .actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #eee;
    padding-top: 10px;
    margin-top: auto;
  }

  .status-message {
    margin-right: 10px;
    font-size: 0.9em;
    color: #666;
  }

  .black-btn {
    background: #000;
    color: #fff;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    cursor: pointer;
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .black-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-left-color: #fff;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  .button-text {
      margin-right: 5px;
  }

  @media (max-width: 768px) {
    .prompt-container {
      flex-direction: column;
      gap: 15px;
    }

    .left-column,
    .right-column {
      width: 100%;
      min-width: 0;
      flex: none;
    }

    h1 {
      margin-top: 0;
    }
  }
</style>
