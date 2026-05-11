import { create } from "zustand";
import type { CostEstimateResponse, SegmentCost, EpisodeCost } from "@/types";

interface CostState {
  costData: CostEstimateResponse | null;
  loading: boolean;
  error: string | null;

  /** Internal indexes — rebuilt on each fetchCost success */
  _segmentIndex: Map<string, SegmentCost>;
  _episodeIndex: Map<number, EpisodeCost>;

  fetchCost: (projectName: string) => Promise<void>;
  debouncedFetch: (projectName: string) => void;
  clear: () => void;

  getEpisodeCost: (episode: number) => EpisodeCost | undefined;
  getSegmentCost: (segmentId: string) => SegmentCost | undefined;
}

let _debounceTimer: ReturnType<typeof setTimeout> | null = null;

export const useCostStore = create<CostState>((set, get) => ({
  costData: null,
  loading: false,
  error: null,
  _segmentIndex: new Map(),
  _episodeIndex: new Map(),

  /** 费用估算已关闭（后端未对接 /cost-estimate 时 SPA 会得到 HTML，解析失败）。占位保持各处 UI 静默无数据。 */
  fetchCost: async (_projectName: string) => {
    set({
      costData: null,
      loading: false,
      error: null,
      _segmentIndex: new Map(),
      _episodeIndex: new Map(),
    });
  },

  debouncedFetch: (projectName: string) => {
    if (_debounceTimer) clearTimeout(_debounceTimer);
    _debounceTimer = null;
    void get().fetchCost(projectName);
  },

  clear: () => {
    if (_debounceTimer) clearTimeout(_debounceTimer);
    _debounceTimer = null;
    set({
      costData: null,
      loading: false,
      error: null,
      _segmentIndex: new Map(),
      _episodeIndex: new Map(),
    });
  },

  getEpisodeCost: (episode: number) => {
    return get()._episodeIndex.get(episode);
  },

  getSegmentCost: (segmentId: string) => {
    return get()._segmentIndex.get(segmentId);
  },
}));
