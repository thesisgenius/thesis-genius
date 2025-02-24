import { request } from "./apiClient";

const thesisAPI = {
  // Thesis CRUD
  createThesis: (data) => request("post", "/thesis/new", data),
  listTheses: () => request("get", "/thesis/theses"),
  getThesis: (id) => request("get", `/thesis/${id}`),
  deleteThesis: (id) => request("delete", `/thesis/${id}`),

  // Cover Page
  getCoverPage: (id) =>
    request("get", `/thesis/${id}/cover-page`).then((d) => d.cover_page),
  updateCoverPage: (id, data) =>
    request("put", `/thesis/${id}/cover-page`, data).then((d) => d.cover_page),

  // Abstract
  getAbstract: (id) => request("get", `/thesis/${id}/abstract`),
  updateAbstract: (id, data) => request("post", `/thesis/${id}/abstract`, data),
  deleteAbstract: (id) => request("delete", `/thesis/${id}/abstract`),

  // Body Pages
  getBodyPages: (id) =>
    request("get", `/thesis/${id}/body-pages`).then((d) => d.body_pages),
  addBodyPage: (id, data) => request("post", `/thesis/${id}/body-pages`, data),
  updateBodyPage: (id, pageId, data) =>
    request("put", `/thesis/${id}/body-pages/${pageId}`, data),
  deleteBodyPage: (id, pageId) =>
    request("delete", `/thesis/${id}/body-pages/${pageId}`),

  // Chapters
  getChapters: (id) =>
    request("get", `/thesis/${id}/chapters`).then((d) => d.chapters),
  getChapter: (id, chapterId) =>
    request("get", `/thesis/${id}/chapters/${chapterId}`),
  addChapter: (id, data) =>
    request("post", `/thesis/${id}/chapters`, data).then((d) => d.chapter),
  updateChapter: (id, chapterId, data) =>
    request("put", `/thesis/${id}/chapters/${chapterId}`, data).then(
      (d) => d.chapter,
    ),
  deleteChapter: (id, chapterId) =>
    request("delete", `/thesis/${id}/chapters/${chapterId}`),

  // Title, Signature, Dedication
  getTitlePage: (id) => request("get", `/thesis/${id}/title`),
  updateTitlePage: (id, data) => request("put", `/thesis/${id}/title`, data),
  getSignaturePage: (id) => request("get", `/thesis/${id}/signature`),
  updateSignaturePage: (id, data) =>
    request("put", `/thesis/${id}/signature`, data),
  getDedicationPage: (id) => request("get", `/thesis/${id}/dedication`),
  updateDedicationPage: (id, data) =>
    request("put", `/thesis/${id}/dedication`, data),

  // TOC, Figures, Tables
  getTableOfContents: (id) => request("get", `/thesis/${id}/table-of-contents`),
  updateTableOfContents: (id, toc) =>
    request("put", `/thesis/${id}/table-of-contents`, {
      table_of_contents: toc,
    }),

  getListOfFigures: (id) => request("get", `/thesis/${id}/list-of-figures`),
  updateListOfFigures: (id, data) =>
    request("put", `/thesis/${id}/list-of-figures`, data),

  getListOfTables: (id) => request("get", `/thesis/${id}/list-of-tables`),
  updateListOfTables: (id, data) =>
    request("put", `/thesis/${id}/list-of-tables`, data),

  // Appendices, References, Copyright
  getAppendices: (id) => request("get", `/thesis/${id}/appendices`),
  updateAppendices: (id, data) =>
    request("put", `/thesis/${id}/appendices`, data),
  getReferences: (id) => request("get", `/thesis/${id}/references`),
  updateReferences: (id, data) =>
    request("put", `/thesis/${id}/references`, data),
  getCopyrightPage: (id) => request("get", `/thesis/${id}/copyright`),
  updateCopyrightPage: (id, data) =>
    request("put", `/thesis/${id}/copyright`, data),

  // Other Info
  getOtherInfo: (id) => request("get", `/thesis/${id}/other-info`),
  updateOtherInfo: (id, data) =>
    request("put", `/thesis/${id}/other-info`, data),

  // Additional
  addFigure: (id, figureData) =>
    request("post", `/thesis/${id}/figures`, figureData),
  deleteFigure: (figureId) => request("delete", `/thesis/figure/${figureId}`),

  exportThesis: (id, format) =>
    request("get", `/format/apa/${id}`, { format }, { responseType: "blob" }),
};

export default thesisAPI;
