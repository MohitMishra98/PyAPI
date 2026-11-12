export interface ScenarioMilestone {
  id: string;
  title: string;
  status: 'completed' | 'in_progress' | 'awaiting_approval' | 'pending';
  duration?: string;
  description: string;
}

export interface ScenarioLog {
  timestamp: string;
  type: 'system' | 'reasoning' | 'tool_call' | 'approval' | 'output';
  message: string;
  tool?: string;
  params?: string;
  vmId?: string;
}

export interface ScenarioApproval {
  required: boolean;
  actionTitle: string;
  impactLevel: 'low' | 'medium' | 'high' | 'critical';
  details: string;
  payloadSummary: { label: string; value: string }[];
}

export interface SimulatorScenario {
  id: string;
  name: string;
  shortDesc: string;
  category: string;
  vmRegion: string;
  goal: string;
  runtimeEstimate: string;
  milestones: ScenarioMilestone[];
  logs: ScenarioLog[];
  approval: ScenarioApproval;
  artifact: {
    title: string;
    type: 'report' | 'diff' | 'spreadsheet';
    content: string;
  };
}

export const SIMULATOR_SCENARIOS: SimulatorScenario[] = [
  {
    id: 'executive-brief',
    name: 'Executive Morning Brief & Calendar Triage',
    shortDesc: 'Scans unread communications, resolves calendar scheduling collisions, and prepares high-context briefing sheets.',
    category: 'Productivity & Leadership',
    vmRegion: 'us-east4-vm-alpha',
    goal: 'Audit 43 unread emails across Gmail, resolve 2 scheduling conflicts in Google Calendar, generate executive briefing memo in Google Docs, and queue Slack digests.',
    runtimeEstimate: '3m 42s autonomous execution',
    milestones: [
      {
        id: 'm1',
        title: 'Ingest and classify communication feeds',
        status: 'completed',
        duration: '18s',
        description: 'Retrieved 43 threads; filtered 4 critical threads requiring immediate principal action.'
      },
      {
        id: 'm2',
        title: 'Detect Calendar conflicts & compute optimal slots',
        status: 'completed',
        duration: '24s',
        description: 'Identified overlap at 2:00 PM EST between Board prep and Product Review; proposed 4:30 PM slot shift.'
      },
      {
        id: 'm3',
        title: 'Synthesize Executive Briefing Document',
        status: 'completed',
        duration: '42s',
        description: 'Compiled synthesized intelligence memo in Google Docs with attached metrics.'
      },
      {
        id: 'm4',
        title: 'Dispatch Slack summary to leadership channel',
        status: 'awaiting_approval',
        description: 'Requires explicit human sign-off before broadcasting to #exec-team and moving calendar invites.'
      }
    ],
    approval: {
      required: true,
      actionTitle: 'Authorize Outbound Broadcast & Schedule Modification',
      impactLevel: 'medium',
      details: 'Spark has prepared the 8:00 AM executive brief and drafted reschedule notifications to 3 participants for the 2:00 PM product review.',
      payloadSummary: [
        { label: 'Recipient Channel', value: '#executive-updates (Slack)' },
        { label: 'Calendar Re-allocations', value: '2:00 PM -> 4:30 PM EST (3 attendees)' },
        { label: 'Attached Document', value: 'Briefing-2026-11-11.gdoc (Cloud Drive)' }
      ]
    },
    logs: [
      { timestamp: '06:00:02', type: 'system', message: 'Spinning up ephemeral cloud container [us-east4-vm-alpha]. Verified zero-leak sandbox.', vmId: 'vm-4892' },
      { timestamp: '06:00:08', type: 'tool_call', tool: 'mcp.workspace.gmail.query', params: '{"label": "INBOX", "unread": true, "max_results": 50}', message: 'Queried unread inbox items; 43 threads fetched successfully.' },
      { timestamp: '06:00:22', type: 'reasoning', message: 'Categorized threads: 2 urgent investor updates, 1 vendor renewal deadline, 40 routine alerts.' },
      { timestamp: '06:00:31', type: 'tool_call', tool: 'mcp.workspace.calendar.list_events', params: '{"time_min": "2026-11-11T08:00:00Z", "time_max": "2026-11-11T20:00:00Z"}', message: 'Fetched calendar schedule; identified 60-minute hard collision at 14:00.' },
      { timestamp: '06:00:54', type: 'tool_call', tool: 'mcp.workspace.docs.create', params: '{"title": "Daily Briefing — Nov 11", "folder": "Executive Memos"}', message: 'Initialized structured memo template with key metric summaries.' },
      { timestamp: '06:01:14', type: 'approval', message: 'HALTED AT CHECKPOINT: Outbound communication requires explicit human-in-the-loop validation.' }
    ],
    artifact: {
      title: 'Daily Executive Briefing — Nov 11, 2026',
      type: 'report',
      content: `# Daily Executive Briefing
**Compiled autonomously by Spark at 06:01 AM EST**
*Dedicated Cloud VM: us-east4-vm-alpha (Sandbox 4892)*

---

### Priority Highlights
- **Series B Bridge Discussion:** Partner Alex Rivera emailed requesting Q3 cohort retention charts before tomorrow's 10:00 AM call. Draft response prepared.
- **Infrastructure Renewal:** AWS compute commitment renewal notice arrives in 4 days. Current utilization efficiency is at 88.4%.

### Calendar Re-alignment
- **Conflict Resolved:** Shifted *Product Design Sync* from 2:00 PM to 4:30 PM to preserve uninterrupted 2-hour *Board Meeting Prep* focus block.
- **Total Focus Time Today:** 4.5 hours scheduled.

### Actions Staged
- [x] Unread communications audited and tagged
- [x] Briefing compiled and synchronized to Google Drive
- [ ] Awaiting approval to ping Slack and dispatch reschedule invites`
    }
  },
  {
    id: 'code-audit',
    name: 'CI/CD Failure Remediation & Security Audit',
    shortDesc: 'Isolates breaking commit in pull request, spins up test container, fixes failing regex vulnerability, and stages pull request.',
    category: 'Engineering & DevOps',
    vmRegion: 'us-central1-vm-gamma',
    goal: 'Diagnose failing integration test on branch feat/auth-v2, patch ReDoS vulnerability in token parser, run local pytest suite, and prepare commit.',
    runtimeEstimate: '4m 12s autonomous execution',
    milestones: [
      {
        id: 'c1',
        title: 'Clone repository & replicate CI failure environment',
        status: 'completed',
        duration: '31s',
        description: 'Isolated test suite failure in tests/test_security_tokens.py:42.'
      },
      {
        id: 'c2',
        title: 'Static analysis & ReDoS vulnerability trace',
        status: 'completed',
        duration: '45s',
        description: 'Pinpointed unescaped catastrophic backtracking pattern in regex helper.'
      },
      {
        id: 'c3',
        title: 'Implement non-backtracking DFA parser & run test suite',
        status: 'completed',
        duration: '52s',
        description: 'All 84 unit and integration tests passing in sandboxed container.'
      },
      {
        id: 'c4',
        title: 'Push hotfix commit and update GitHub Pull Request #419',
        status: 'awaiting_approval',
        description: 'Requires security lead approval prior to pushing commit upstream.'
      }
    ],
    approval: {
      required: true,
      actionTitle: 'Authorize Git Push to Origin / PR #419',
      impactLevel: 'high',
      details: 'Spark has written the fix for CVE-2026-8819 and verified 84 tests pass cleanly. Awaiting approval to push branch and ping reviewers.',
      payloadSummary: [
        { label: 'Target Branch', value: 'origin/feat/auth-v2' },
        { label: 'Files Modified', value: 'src/auth/token_validator.ts (+14 -8)' },
        { label: 'Test Suite Result', value: '84 passed, 0 failed, 100% assertions green' }
      ]
    },
    logs: [
      { timestamp: '14:22:01', type: 'system', message: 'Spawning isolated Linux VM container with Docker-in-Docker enabled.', vmId: 'vm-9921' },
      { timestamp: '14:22:15', type: 'tool_call', tool: 'mcp.github.repo.clone', params: '{"ref": "feat/auth-v2", "depth": 1}', message: 'Repository cloned into /tmp/sandbox-repo.' },
      { timestamp: '14:22:42', type: 'tool_call', tool: 'mcp.terminal.exec', params: '{"cmd": "npm test -- --filter tokens"}', message: 'Replicated failure: ReDoS timeout on edge-case payload (10,480ms).' },
      { timestamp: '14:23:10', type: 'reasoning', message: 'Replacing recursive regex pattern with atomic string indexing token scanner.' },
      { timestamp: '14:23:38', type: 'tool_call', tool: 'mcp.terminal.exec', params: '{"cmd": "npm test"}', message: 'Re-ran suite: 84/84 tests passed in 1,220ms.' },
      { timestamp: '14:24:02', type: 'approval', message: 'HALTED AT CHECKPOINT: Git push to remote repository requires manual sign-off.' }
    ],
    artifact: {
      title: 'Code Patch: token_validator.ts (Diff)',
      type: 'diff',
      content: `--- a/src/auth/token_validator.ts
+++ b/src/auth/token_validator.ts
@@ -38,8 +38,14 @@ export function validateSignature(header: string): boolean {
-  // Vulnerable to catastrophic backtracking
-  const pattern = /^([a-zA-Z0-9_-]+\\.)*([a-zA-Z0-9_-]+)$/;
-  return pattern.test(header);
+  // Linear O(n) token verification with strict segment boundaries
+  const segments = header.split('.');
+  if (segments.length !== 3) return false;
+  for (let i = 0; i < segments.length; i++) {
+    if (!/^[a-zA-Z0-9_-]+$/.test(segments[i])) return false;
+  }
+  return true;
 }`
    }
  },
  {
    id: 'customer-retention',
    name: 'Customer Churn Prevention & Executive Outreach',
    shortDesc: 'Monitors Stripe events and product telemetry to identify churning accounts and stages personalized re-engagement campaigns.',
    category: 'Revenue & Operations',
    vmRegion: 'eu-west1-vm-beta',
    goal: 'Identify enterprise accounts with >40% usage drop in past 14 days, aggregate telemetry from PostgreSQL, and prepare tailored CEO outreach email in Gmail.',
    runtimeEstimate: '5m 10s autonomous execution',
    milestones: [
      {
        id: 'r1',
        title: 'Run PostgreSQL analytical query across usage events',
        status: 'completed',
        duration: '14s',
        description: 'Analyzed 1.2M event logs across 180 active enterprise workspaces.'
      },
      {
        id: 'r2',
        title: 'Cross-reference billing tiers in Stripe API',
        status: 'completed',
        duration: '19s',
        description: 'Identified Acme Corp ($48,000 ARR) experiencing seat inactivity.'
      },
      {
        id: 'r3',
        title: 'Synthesize custom diagnostics & solution blueprint',
        status: 'completed',
        duration: '38s',
        description: 'Detected breaking integration on their custom webhook endpoint as root cause.'
      },
      {
        id: 'r4',
        title: 'Stage proactive executive outreach email in Gmail',
        status: 'awaiting_approval',
        description: 'Requires VP of Customer Success sign-off prior to external delivery.'
      }
    ],
    approval: {
      required: true,
      actionTitle: 'Authorize Outbound Executive Retention Email',
      impactLevel: 'high',
      details: 'Spark has pinpointed that Acme Corp’s webhook broke on Nov 8, causing their drop in active users. A proactive, solution-oriented outreach email is staged in your drafts.',
      payloadSummary: [
        { label: 'Recipient', value: 'dan.reynolds@acmecorp.com (VP Engineering)' },
        { label: 'Subject', value: 'Quick heads up: We spotted a webhook issue on your Spark endpoint' },
        { label: 'Account ARR', value: '$48,000 / year' }
      ]
    },
    logs: [
      { timestamp: '09:15:00', type: 'system', message: 'Cron trigger [daily-churn-monitor] initiated on eu-west1-vm-beta.', vmId: 'vm-3104' },
      { timestamp: '09:15:12', type: 'tool_call', tool: 'mcp.db.postgres.query', params: '{"sql": "SELECT org_id, count(*) FROM telemetry GROUP BY org_id HAVING..."}', message: 'Query executed in 410ms; returned 1 outlier organization.' },
      { timestamp: '09:15:31', type: 'tool_call', tool: 'mcp.stripe.customers.retrieve', params: '{"customer_id": "cus_9938A"}', message: 'Customer record retrieved: Enterprise Annual Plan, renews Dec 2026.' },
      { timestamp: '09:16:04', type: 'reasoning', message: 'Root cause identified: HTTP 502 Bad Gateway responses from customer endpoint since latest release.' },
      { timestamp: '09:16:40', type: 'tool_call', tool: 'mcp.workspace.gmail.create_draft', params: '{"to": "dan.reynolds@acmecorp.com"}', message: 'Draft created with diagnostic logs attached.' },
      { timestamp: '09:17:05', type: 'approval', message: 'HALTED AT CHECKPOINT: External outbound email to strategic account requires confirmation.' }
    ],
    artifact: {
      title: 'Staged Email Draft — Acme Corp Retention Outreach',
      type: 'report',
      content: `**To:** dan.reynolds@acmecorp.com
**Subject:** Quick heads up regarding your webhook sync on Spark
**From:** Sarah Lin <sarah@ourcompany.com>

Hi Dan,

Our autonomous monitoring system noticed that Acme Corp's daily data pipeline sync has been experiencing intermittent HTTP 502 gateway timeouts over the last 72 hours, resulting in dropped events.

We ran a diagnostic in our sandbox: your team's endpoint is expecting a payload format with \`v2_schema: true\`. 

I've attached the exact request trace and an easy 2-line config patch your engineers can apply immediately. Let me know if you'd like our solutions engineer to jump on a 10-minute huddle today to get this green.

Best,
Sarah Lin
Head of Solutions`
    }
  }
];

export const CORE_FEATURES = [
  {
    icon: 'CloudRain',
    title: '24/7 Cloud Sandbox Execution',
    highlight: 'Persistent Runtime',
    description: 'Spark runs on dedicated, ephemeral cloud virtual machines. It keeps working across hours or days while your laptop is closed, your phone is locked, or you are completely offline.'
  },
  {
    icon: 'GitFork',
    title: 'Milestone Decomposition Engine',
    highlight: 'Deterministic Graphs',
    description: 'Give Spark an ambitious objective. Its reasoning engine splits high-level goals into ordered micro-milestones, checking prerequisites and adapting when unexpected blockers occur.'
  },
  {
    icon: 'ShieldCheck',
    title: 'Human-in-the-Loop Safe Autonomy',
    highlight: 'Zero Rogue Actions',
    description: 'Spark operates with total freedom on safe actions (researching, computing, staging, synthesizing), but automatically halts at checkpoints for your one-click approval on high-impact operations.'
  },
  {
    icon: 'Network',
    title: 'Model Context Protocol (MCP) Native',
    highlight: 'Universal Tool Standard',
    description: 'Connect any tool in minutes. Spark integrates natively with Google Workspace, Slack, Linear, GitHub, Stripe, PostgreSQL, and any custom MCP server with zero glue code.'
  },
  {
    icon: 'Clock',
    title: 'Cron Schedules & Event Triggers',
    highlight: 'Continuous Intelligence',
    description: 'Set recurring workflows that awaken on schedule—compiling morning briefings, running weekly security sweeps, or monitoring competitive market movements while you sleep.'
  },
  {
    icon: 'BrainCircuit',
    title: 'Adaptive Procedural Memory',
    highlight: 'Reusable Skills',
    description: 'Instruct Spark once on your team’s tone, PR guidelines, or escalation protocol. Spark compiles it into reusable skills that persist deterministically across all future workflows.'
  }
];

export const INTEGRATIONS = [
  { name: 'Google Workspace', category: 'Productivity', count: 'Gmail, Drive, Docs, Sheets, Calendar', logo: 'Google' },
  { name: 'GitHub & GitLab', category: 'DevOps', count: 'PRs, Issues, Actions, Code Review', logo: 'Git' },
  { name: 'Slack & Teams', category: 'Communication', count: 'Live Channels, DMs, Threads, Bots', logo: 'Slack' },
  { name: 'Linear & Jira', category: 'Project Mgmt', count: 'Sprint Planning, Auto-triage, Milestones', logo: 'Linear' },
  { name: 'PostgreSQL & Snowflake', category: 'Databases', count: 'SQL Execution, Schema Inspection', logo: 'Database' },
  { name: 'Stripe & HubSpot', category: 'Business Ops', count: 'Subscriptions, CRM Updates, Churn Alerts', logo: 'Stripe' },
  { name: 'Custom MCP Servers', category: 'Extensible', count: 'Any REST / GraphQL / gRPC Service', logo: 'Code' },
  { name: 'Cloud Browser Sandbox', category: 'Web Automation', count: 'Headless Chromium, Authenticated Sessions', logo: 'Globe' }
];

export const COMPARISON_ROWS = [
  {
    feature: 'Execution Persistence',
    traditional: 'Halted immediately when browser tab or laptop closes',
    spark: 'Always-on 24/7 dedicated cloud VM runtime',
    isWin: true
  },
  {
    feature: 'Multi-Step Execution Horizon',
    traditional: 'Single prompt-response loop; user must hand-hold every prompt',
    spark: 'Autonomous multi-day milestone decomposition & execution',
    isWin: true
  },
  {
    feature: 'Action Safety & Approvals',
    traditional: 'Either completely blocked or triggers blind uncontrolled API calls',
    spark: 'Deterministic human-in-the-loop checkpoints with 1-tap review',
    isWin: true
  },
  {
    feature: 'Tool Extensibility',
    traditional: 'Locked to vendor walled-gardens with rigid plugins',
    spark: 'Open Model Context Protocol (MCP) + secure custom VM environments',
    isWin: true
  },
  {
    feature: 'Scheduled Recurring Workflows',
    traditional: 'Requires manual initiation every single time',
    spark: 'Native cron schedules, webhook listeners & event-driven triggers',
    isWin: true
  },
  {
    feature: 'Skill & Tone Customization',
    traditional: 'Lost between context windows; prompt templates reset',
    spark: 'Persistent procedural skills stored in team operational memory',
    isWin: true
  }
];

export const PRICING_PLANS = [
  {
    name: 'Developer',
    badge: 'Individual Builder',
    priceMonthly: 39,
    priceAnnual: 29,
    description: 'For solo developers, technical founders, and operators looking to automate complex daily execution.',
    features: [
      '3 concurrent autonomous cloud sandboxes',
      'Up to 40 background execution hours / month',
      'Google Workspace & GitHub MCP connectors',
      'Telegram, Email & Webhook approval triggers',
      '5 persistent procedural skills',
      'Standard community support'
    ],
    popular: false,
    cta: 'Start 14-Day Free Trial'
  },
  {
    name: 'Team',
    badge: 'Most Popular',
    priceMonthly: 119,
    priceAnnual: 89,
    description: 'For high-velocity engineering, product, and leadership teams scaling autonomous workflows.',
    features: [
      '15 concurrent autonomous cloud sandboxes',
      '250 background execution hours / month',
      'All native MCP connectors + Custom MCP servers',
      'Instant 1-tap Slack & Discord approvals',
      'Unlimited shared team procedural skills',
      'Sub-minute cron schedules & webhooks',
      'Priority VM allocation (<100ms cold start)',
      'Shared team workspace & audit logs'
    ],
    popular: true,
    cta: 'Get Started with Team'
  },
  {
    name: 'Enterprise Fleet',
    badge: 'Custom Governance',
    priceMonthly: null,
    priceAnnual: null,
    description: 'For organizations demanding dedicated VPC sandboxes, custom LLM routing, and strict SOC 2 compliance.',
    features: [
      'Unlimited dedicated VPC cloud sandboxes',
      'Custom LLM model routing (Bring Your Own Keys / On-Prem)',
      'Custom SLA with 99.99% uptime guarantee',
      'Single Sign-On (SAML/Okta) & SCIM provisioning',
      'Dedicated Customer Success & Solutions Architect',
      'Custom security reviews & BAA agreements'
    ],
    popular: false,
    cta: 'Speak with Enterprise Team'
  }
];

export const TESTIMONIALS = [
  {
    quote: 'Spark operates in a completely different category. While other tools wait for me to type another prompt, Spark finishes an 8-hour sprint audit and dependency upgrade while I am sleeping on a red-eye flight.',
    author: 'Elena Rostova',
    role: 'VP of Engineering',
    company: 'Vanguard Systems',
    metric: '18 hours saved weekly / engineer'
  },
  {
    quote: 'The human-in-the-loop approval mechanism gave our compliance team the confidence to let Spark touch customer communications and billing systems. Zero rogue errors in over 6 months.',
    author: 'Marcus Vance',
    role: 'Chief of Staff',
    company: 'HyperScale Health',
    metric: '99.8% precision rate'
  },
  {
    quote: 'Our morning executive brief used to take two analysts 90 minutes every dawn. Spark compiles the entire portfolio health report, verifies the numbers, and has it in my inbox before 6:00 AM.',
    author: 'Devon Kester',
    role: 'Managing Partner',
    company: 'Aura Capital',
    metric: '$140k annual operational savings'
  }
];

export const FAQS = [
  {
    question: 'How is Spark different from conversational chat assistants?',
    answer: 'Standard chatbots are reactive: they pause execution the moment you navigate away or shut your laptop, and they cannot execute continuous multi-hour objectives. Spark runs in persistent, dedicated cloud virtual machines (VMs). You define the goal, and Spark decomposes it into milestones, executes tool calls, monitors progress, and operates 24/7 in the cloud—even when you are completely offline.'
  },
  {
    question: 'How do human-in-the-loop approvals work?',
    answer: 'Spark categorizes every planned action by impact level. Low-risk operations (such as reading documents, running tests, querying databases, drafting content) execute autonomously. High-impact operations (such as sending external emails, updating production databases, or committing code to upstream branches) halt at deterministic checkpoints. You receive an instantaneous notification via Slack, Telegram, or Web push with an exact visual diff, which you can approve or revise in one tap.'
  },
  {
    question: 'What is the Model Context Protocol (MCP) and how does Spark use it?',
    answer: 'Model Context Protocol (MCP) is the open industry standard for connecting AI agents to tools, APIs, and data sources safely. Spark implements MCP natively, allowing it to seamlessly talk to Google Workspace, GitHub, Slack, Linear, PostgreSQL, and any custom MCP server your company hosts—without brittle proprietary integrations.'
  },
  {
    question: 'Where do the cloud sandboxes execute and is my data secure?',
    answer: 'Every workflow runs in an ephemeral, firewalled container provisioned on secure cloud infrastructure. The sandbox is completely destroyed upon task completion. We enforce end-to-end encryption in transit (TLS 1.3) and at rest (AES-256-GCM), with SOC 2 Type II compliance and zero data retention for model training.'
  },
  {
    question: 'Can I set tasks to run on recurring schedules or webhooks?',
    answer: 'Yes. Spark provides built-in cron scheduling and webhook triggers. You can configure agents to wake up every morning at 7:00 AM to summarize customer feedback, run nightly security audits, or trigger automatically whenever a high-priority customer ticket is created.'
  },
  {
    question: 'Can I train Spark on our internal SOPs and team guidelines?',
    answer: 'Yes. With Spark Procedural Skills, you can define guidelines once—such as your pull request review checklist, brand communication tone, or financial reporting format. Spark stores these as reusable operational memories and applies them across every relevant workflow.'
  }
];
