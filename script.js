// Supported language list used across the translator UI.
const languageMap = {
  English: 'English',
  'Juba Arabic': 'Juba Arabic',
  Dinka: 'Dinka',
  Nuer: 'Nuer',
  Bari: 'Bari',
  Zande: 'Zande',
  Shilluk: 'Shilluk',
  Toposa: 'Toposa',
  Acholi: 'Acholi',
  Murle: 'Murle'
};

// Demo translation data for the frontend-only translation experience.
const sampleTranslations = {
  English: {
    Dinka: 'Aŋɔk awɛr',
    'Juba Arabic': 'أهلاً',
    Nuer: 'Ayi',
    Bari: 'Ayi'
  },
  Dinka: {
    English: 'Welcome',
    'Juba Arabic': 'أهلاً'
  }
};

const nav = document.querySelector('.nav');
const navToggle = document.querySelector('.nav-toggle');
const themeToggle = document.getElementById('themeToggle');
const themeCycleBtn = document.getElementById('themeCycleBtn');
const sourceText = document.getElementById('sourceText');
const resultText = document.getElementById('resultText');
const sourceCount = document.getElementById('sourceCount');
const translateBtn = document.getElementById('translateBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');
const swapBtn = document.getElementById('swapBtn');
const sampleBtn = document.getElementById('sampleBtn');
const sourceLang = document.getElementById('sourceLanguage');
const targetLang = document.getElementById('targetLanguage');
const contactForm = document.getElementById('contactForm');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const registerPassword = document.getElementById('registerPassword');
const passwordStrength = document.getElementById('passwordStrength');
const registerConfirmPassword = document.getElementById('registerConfirmPassword');
const contactMessageOutput = document.getElementById('contactMessageOutput');

function setActiveNav() {
  const currentPage = document.body.dataset.page;
  document.querySelectorAll('.nav-link').forEach((link) => {
    const href = link.getAttribute('href');
    const pageName = href.replace('.html', '').replace('./', '');
    const isHome = (currentPage === 'home' || currentPage === 'index') && pageName === 'index';

    if (href && (currentPage === pageName || isHome)) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

function initTheme() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') {
    document.documentElement.classList.add('dark');
  } else if (saved === 'sunrise') {
    document.documentElement.classList.add('theme-sunrise');
  } else if (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark');
  }
  updateThemeButton();
}

function updateThemeButton() {
  if (!themeToggle) return;
  const isDark = document.documentElement.classList.contains('dark');
  const isSunrise = document.documentElement.classList.contains('theme-sunrise');
  if (isDark) {
    themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
  } else if (isSunrise) {
    themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
  } else {
    themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
  }
}

function toggleTheme() {
  const root = document.documentElement;
  if (root.classList.contains('theme-sunrise')) {
    root.classList.remove('theme-sunrise');
    root.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else if (root.classList.contains('dark')) {
    root.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  } else {
    root.classList.add('theme-sunrise');
    localStorage.setItem('theme', 'sunrise');
  }
  updateThemeButton();
}

function updateCount() {
  if (!sourceText || !sourceCount) return;
  sourceCount.textContent = `${sourceText.value.length}/500`;
}

function getDummyTranslation(text, source, target) {
  if (!text.trim()) return '';
  const textLower = text.trim().toLowerCase();
  const base = sampleTranslations[source]?.[target];
  if (base) return base;
  if (textLower.includes('hello')) return target === 'Dinka' ? 'Aŋɔk' : 'Hello';
  if (textLower.includes('thank')) return target === 'Dinka' ? 'Aciɛr' : 'Thank you';
  if (textLower.includes('welcome')) return target === 'Dinka' ? 'Aŋɔk' : 'Welcome';
  return `${text.trim()} [translated to ${target}]`;
}

function translateText() {
  if (!sourceText || !resultText) return;
  const text = sourceText.value.trim();
  if (!text) {
    resultText.value = '';
    return;
  }
  const source = sourceLang.value;
  const target = targetLang.value;
  resultText.value = getDummyTranslation(text, source, target);
}

function swapLanguages() {
  const temp = sourceLang.value;
  sourceLang.value = targetLang.value;
  targetLang.value = temp;
  const tempText = sourceText.value;
  sourceText.value = resultText.value;
  resultText.value = tempText;
  updateCount();
}

function copyTranslation() {
  if (!resultText.value) return;
  navigator.clipboard.writeText(resultText.value);
  copyBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
  setTimeout(() => {
    copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i>';
  }, 1500);
}

function clearText() {
  sourceText.value = '';
  resultText.value = '';
  updateCount();
}

function validateContactForm(event) {
  event.preventDefault();
  const name = document.getElementById('contactName').value.trim();
  const email = document.getElementById('contactEmail').value.trim();
  const subject = document.getElementById('contactSubject').value.trim();
  const message = document.getElementById('contactMessage').value.trim();

  if (!name || !email || !subject || !message) {
    contactMessageOutput.textContent = 'Please fill in all fields.';
    contactMessageOutput.style.color = 'red';
    return;
  }

  if (!email.includes('@')) {
    contactMessageOutput.textContent = 'Please enter a valid email.';
    contactMessageOutput.style.color = 'red';
    return;
  }

  contactMessageOutput.textContent = 'Thanks for reaching out! We will contact you soon.';
  contactMessageOutput.style.color = 'green';
  contactForm.reset();
}

function checkPasswordStrength() {
  const value = registerPassword.value;
  let strength = 'Weak';
  let color = 'red';
  if (value.length >= 8 && /[A-Z]/.test(value) && /[0-9]/.test(value)) {
    strength = 'Strong';
    color = 'green';
  } else if (value.length >= 6) {
    strength = 'Medium';
    color = 'orange';
  }
  passwordStrength.textContent = `Password strength: ${strength}`;
  passwordStrength.style.color = color;
}

function validateRegisterForm(event) {
  event.preventDefault();
  const password = registerPassword.value;
  const confirm = registerConfirmPassword.value;
  if (password !== confirm) {
    passwordStrength.textContent = 'Passwords do not match.';
    passwordStrength.style.color = 'red';
    return;
  }
  if (!document.getElementById('agreeTerms').checked) {
    passwordStrength.textContent = 'Please agree to the terms.';
    passwordStrength.style.color = 'red';
    return;
  }
  passwordStrength.textContent = 'Registration successful!';
  passwordStrength.style.color = 'green';
  registerForm.reset();
}

if (navToggle && nav) {
  navToggle.addEventListener('click', () => nav.classList.toggle('open'));
}

if (themeToggle) {
  themeToggle.addEventListener('click', toggleTheme);
}

if (themeCycleBtn) {
  themeCycleBtn.addEventListener('click', toggleTheme);
}

if (sourceText) {
  sourceText.addEventListener('input', () => {
    updateCount();
  });
}

if (translateBtn) {
  translateBtn.addEventListener('click', translateText);
}

if (clearBtn) {
  clearBtn.addEventListener('click', clearText);
}

if (copyBtn) {
  copyBtn.addEventListener('click', copyTranslation);
}

if (swapBtn) {
  swapBtn.addEventListener('click', swapLanguages);
}

if (sampleBtn) {
  sampleBtn.addEventListener('click', () => {
    sourceText.value = 'Welcome to South Sudan';
    sourceLang.value = 'English';
    targetLang.value = 'Dinka';
    updateCount();
    translateText();
  });
}

if (contactForm) {
  contactForm.addEventListener('submit', validateContactForm);
}

if (loginForm) {
  loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    window.location.href = 'dashboard.html';
  });
}

if (registerForm) {
  registerForm.addEventListener('submit', validateRegisterForm);
}

if (registerPassword) {
  registerPassword.addEventListener('input', checkPasswordStrength);
}

function revealOnScroll() {
  document.querySelectorAll('.scroll-reveal').forEach((element) => {
    const position = element.getBoundingClientRect().top;
    if (position < window.innerHeight * 0.9) {
      element.classList.add('visible');
    }
  });
}

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', revealOnScroll);

setActiveNav();
initTheme();
updateCount();
revealOnScroll();
