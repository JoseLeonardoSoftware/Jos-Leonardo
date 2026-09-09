const MS_PER_DAY = 24 * 60 * 60 * 1000;
const MAX_TASKS_PER_DAY = 5;
const MIN_TASKS_PER_DAY = 3;

const LEVEL_WEIGHTS = {
  iniciante: 0,
  intermediario: 1,
  avançado: 2,
  avancado: 2
};

const AREA_CATALOG = {
  backend: [
    { title: "Lógica de programação", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "HTTP e arquitetura cliente-servidor", difficulty: "fundamentos", priority: 1, minutes: 75 },
    { title: "JavaScript moderno para backend", difficulty: "fundamentos", priority: 1, minutes: 80 },
    { title: "Node.js e NPM", difficulty: "fundamentos", priority: 2, minutes: 80 },
    { title: "APIs REST e padrões de rotas", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Banco de dados SQL", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Autenticação e segurança", difficulty: "intermediario", priority: 3, minutes: 80 },
    { title: "Testes, logs e deploy", difficulty: "avancado", priority: 3, minutes: 90 }
  ],
  frontend: [
    { title: "HTML semântico", difficulty: "fundamentos", priority: 1, minutes: 60 },
    { title: "CSS responsivo", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "JavaScript para interfaces", difficulty: "fundamentos", priority: 1, minutes: 80 },
    { title: "Acessibilidade e UX", difficulty: "fundamentos", priority: 2, minutes: 70 },
    { title: "React e componentização", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Estado, formulários e consumo de API", difficulty: "intermediario", priority: 2, minutes: 90 },
    { title: "Performance e arquitetura", difficulty: "avancado", priority: 3, minutes: 90 },
    { title: "Testes de interface e deploy", difficulty: "avancado", priority: 3, minutes: 80 }
  ],
  dados: [
    { title: "Lógica e estatística básica", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "Python para análise", difficulty: "fundamentos", priority: 1, minutes: 80 },
    { title: "SQL e modelagem de dados", difficulty: "fundamentos", priority: 1, minutes: 85 },
    { title: "Limpeza e exploração de dados", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Visualização com dashboards", difficulty: "intermediario", priority: 2, minutes: 80 },
    { title: "Probabilidade e inferência", difficulty: "intermediario", priority: 2, minutes: 90 },
    { title: "Machine learning introdutório", difficulty: "avancado", priority: 3, minutes: 95 },
    { title: "Projetos e storytelling analítico", difficulty: "avancado", priority: 3, minutes: 85 }
  ],
  enem: [
    { title: "Leitura e interpretação", difficulty: "fundamentos", priority: 1, minutes: 60 },
    { title: "Redação: repertório e estrutura", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "Matemática básica e porcentagem", difficulty: "fundamentos", priority: 1, minutes: 80 },
    { title: "Ciências da natureza", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Ciências humanas", difficulty: "intermediario", priority: 2, minutes: 75 },
    { title: "Questões cronometradas", difficulty: "intermediario", priority: 2, minutes: 90 },
    { title: "Simulados e correção", difficulty: "avancado", priority: 3, minutes: 95 },
    { title: "Revisão final por incidência", difficulty: "avancado", priority: 3, minutes: 80 }
  ],
  concursos: [
    { title: "Português e interpretação", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "Raciocínio lógico", difficulty: "fundamentos", priority: 1, minutes: 75 },
    { title: "Direito administrativo", difficulty: "fundamentos", priority: 1, minutes: 85 },
    { title: "Direito constitucional", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Informática", difficulty: "intermediario", priority: 2, minutes: 70 },
    { title: "Questões comentadas", difficulty: "intermediario", priority: 2, minutes: 90 },
    { title: "Simulados por banca", difficulty: "avancado", priority: 3, minutes: 95 },
    { title: "Revisões estratégicas", difficulty: "avancado", priority: 3, minutes: 80 }
  ],
  default: [
    { title: "Mapeamento dos fundamentos", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "Prática guiada", difficulty: "fundamentos", priority: 1, minutes: 70 },
    { title: "Consolidação conceitual", difficulty: "intermediario", priority: 2, minutes: 80 },
    { title: "Projetos e exercícios", difficulty: "intermediario", priority: 2, minutes: 85 },
    { title: "Domínio avançado", difficulty: "avancado", priority: 3, minutes: 90 }
  ]
};

function normalizeArea(area = "") {
  const normalized = area.trim().toLowerCase();
  return AREA_CATALOG[normalized] ? normalized : "default";
}

function startOfDay(date) {
  const value = new Date(date);
  value.setHours(0, 0, 0, 0);
  return value;
}

function toIsoDate(date) {
  return startOfDay(date).toISOString().split("T")[0];
}

function addDays(date, days) {
  return new Date(startOfDay(date).getTime() + days * MS_PER_DAY);
}

function diffDays(a, b) {
  return Math.ceil((startOfDay(b).getTime() - startOfDay(a).getTime()) / MS_PER_DAY);
}

function deriveWeeks(profile) {
  if (profile.goalType === "weeks" && Number(profile.goalWeeks) > 0) {
    return Math.max(2, Number(profile.goalWeeks));
  }

  if (profile.goalDate) {
    const today = startOfDay(new Date());
    const days = diffDays(today, profile.goalDate);
    return Math.max(2, Math.ceil(days / 7));
  }

  return 8;
}

function buildModules(area, level) {
  const levelWeight = LEVEL_WEIGHTS[level] ?? 0;
  const modules = AREA_CATALOG[normalizeArea(area)]
    .slice()
    .sort((a, b) => a.priority - b.priority);

  if (levelWeight === 0) {
    return modules;
  }

  if (levelWeight === 1) {
    return modules.filter((item) => item.difficulty !== "avancado").concat(
      modules.filter((item) => item.difficulty === "avancado")
    );
  }

  return modules
    .filter((item) => item.difficulty !== "fundamentos")
    .concat(modules.filter((item) => item.difficulty === "fundamentos"));
}

function createStudyTasks({ modules, totalDays, dailyHours }) {
  const availableMinutes = Math.max(60, Math.round(dailyHours * 60));
  const targetTasksPerDay = Math.max(
    MIN_TASKS_PER_DAY,
    Math.min(MAX_TASKS_PER_DAY, Math.round(availableMinutes / 45))
  );
  const totalTaskSlots = Math.max(totalDays * targetTasksPerDay, modules.length * 2);

  const baseTasks = [];
  let cursor = 0;

  while (baseTasks.length < totalTaskSlots) {
    const module = modules[cursor % modules.length];
    const cycle = Math.floor(cursor / modules.length);
    const stage = cycle === 0 ? "Aprender" : cycle === 1 ? "Praticar" : "Aprofundar";

    baseTasks.push({
      id: `task-${baseTasks.length + 1}`,
      title: `${stage}: ${module.title}`,
      topic: module.title,
      type: cycle === 0 ? "study" : "practice",
      difficulty: module.difficulty,
      priority: module.priority,
      estimatedMinutes: Math.min(module.minutes + cycle * 5, availableMinutes),
      completed: false
    });

    if (cycle === 0) {
      baseTasks.push({
        id: `task-${baseTasks.length + 1}`,
        title: `Revisão espaçada: ${module.title}`,
        topic: module.title,
        type: "review",
        difficulty: module.difficulty,
        priority: module.priority,
        estimatedMinutes: Math.min(35, Math.round(module.minutes / 2)),
        completed: false,
        spacedOffsetDays: 3
      });
    }

    if (cycle === 1) {
      baseTasks.push({
        id: `task-${baseTasks.length + 1}`,
        title: `Revisão profunda: ${module.title}`,
        topic: module.title,
        type: "review",
        difficulty: module.difficulty,
        priority: module.priority + 1,
        estimatedMinutes: Math.min(45, Math.round(module.minutes / 1.8)),
        completed: false,
        spacedOffsetDays: 10
      });
    }

    cursor += 1;
  }

  return baseTasks.slice(0, totalTaskSlots + modules.length);
}

function createEmptyDays(totalDays, startDate, dailyHours) {
  return Array.from({ length: totalDays }, (_, index) => ({
    date: toIsoDate(addDays(startDate, index)),
    estimatedHours: Number(dailyHours),
    tasks: []
  }));
}

function allocateTasksToDays(tasks, days) {
  tasks.forEach((task, index) => {
    let targetIndex = index % days.length;

    if (task.type === "review" && Number.isInteger(task.spacedOffsetDays)) {
      targetIndex = Math.min(days.length - 1, index + task.spacedOffsetDays);
    }

    let bestIndex = targetIndex;

    for (let step = 0; step < days.length; step += 1) {
      const probe = (targetIndex + step) % days.length;
      if (days[probe].tasks.length < MAX_TASKS_PER_DAY) {
        bestIndex = probe;
        break;
      }
    }

    days[bestIndex].tasks.push(task);
  });

  return days.map((day) => {
    const orderedTasks = day.tasks
      .slice()
      .sort((a, b) => a.priority - b.priority || a.estimatedMinutes - b.estimatedMinutes);

    return {
      ...day,
      tasks: orderedTasks.slice(0, MAX_TASKS_PER_DAY)
    };
  });
}

function groupIntoWeeks(days) {
  const weeks = [];

  days.forEach((day, index) => {
    const weekIndex = Math.floor(index / 7);
    if (!weeks[weekIndex]) {
      weeks[weekIndex] = {
        weekNumber: weekIndex + 1,
        focus: "",
        days: []
      };
    }

    weeks[weekIndex].days.push(day);
  });

  return weeks.map((week) => {
    const tasks = week.days.flatMap((day) => day.tasks);
    const topTopics = [...new Set(tasks.slice(0, 3).map((task) => task.topic))];

    return {
      ...week,
      startDate: week.days[0]?.date,
      endDate: week.days[week.days.length - 1]?.date,
      focus: topTopics.length ? topTopics.join(" • ") : "Consolidação e revisão"
    };
  });
}

function computeSummary(weeks) {
  const tasks = weeks.flatMap((week) => week.days.flatMap((day) => day.tasks));
  const completedTasks = tasks.filter((task) => task.completed).length;
  const totalMinutes = tasks.reduce((sum, task) => sum + task.estimatedMinutes, 0);
  const reviewTasks = tasks.filter((task) => task.type === "review").length;

  return {
    totalWeeks: weeks.length,
    totalTasks: tasks.length,
    completedTasks,
    completionRate: tasks.length ? Math.round((completedTasks / tasks.length) * 100) : 0,
    reviewTasks,
    totalStudyHours: Number((totalMinutes / 60).toFixed(1))
  };
}

export function generateRoadmap(profile) {
  const today = startOfDay(new Date());
  const totalWeeks = deriveWeeks(profile);
  const totalDays = totalWeeks * 7;
  const modules = buildModules(profile.area, profile.level);
  const tasks = createStudyTasks({
    modules,
    totalDays,
    dailyHours: Number(profile.dailyHours)
  });
  const emptyDays = createEmptyDays(totalDays, today, profile.dailyHours);
  const allocatedDays = allocateTasksToDays(tasks, emptyDays);
  const weeks = groupIntoWeeks(allocatedDays);

  return {
    id: `roadmap-${Date.now()}`,
    generatedAt: new Date().toISOString(),
    profile: {
      ...profile,
      goalWeeks: totalWeeks
    },
    weeks,
    summary: computeSummary(weeks)
  };
}

function flattenPendingTasks(roadmap) {
  return roadmap.weeks.flatMap((week) =>
    week.days.flatMap((day) =>
      day.tasks
        .filter((task) => !task.completed)
        .map((task) => ({
          ...task,
          originalDate: day.date
        }))
    )
  );
}

export function recalculateRoadmap(roadmap, options = {}) {
  const referenceDate = options.referenceDate
    ? startOfDay(options.referenceDate)
    : startOfDay(new Date());
  const futureDays = roadmap.weeks
    .flatMap((week) => week.days)
    .filter((day) => startOfDay(day.date) >= referenceDate)
    .map((day) => ({
      ...day,
      tasks: []
    }));

  if (!futureDays.length) {
    return {
      ...roadmap,
      recalculatedAt: new Date().toISOString(),
      summary: computeSummary(roadmap.weeks)
    };
  }

  const completedByDate = new Map();
  roadmap.weeks.forEach((week) => {
    week.days.forEach((day) => {
      const done = day.tasks.filter((task) => task.completed);
      if (done.length) {
        completedByDate.set(day.date, {
          ...day,
          tasks: done
        });
      }
    });
  });

  const pendingTasks = flattenPendingTasks(roadmap);
  allocateTasksToDays(
    pendingTasks.map((task, index) => ({
      ...task,
      id: `${task.id}-r${index + 1}`
    })),
    futureDays
  );

  const mergedDays = roadmap.weeks
    .flatMap((week) => week.days)
    .map((day) => completedByDate.get(day.date) || futureDays.find((future) => future.date === day.date) || day);

  const weeks = groupIntoWeeks(mergedDays);

  return {
    ...roadmap,
    recalculatedAt: new Date().toISOString(),
    weeks,
    summary: computeSummary(weeks)
  };
}
